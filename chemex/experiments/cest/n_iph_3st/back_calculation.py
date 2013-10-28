"""
Created on Aug 15, 2011

@author: guillaume
"""

# Python Modules
import scipy as sc
from scipy.linalg import expm

# Local Modules
# from chemex.experiments.misc import correct_chemical_shift
from chemex.caching import lru_cache
from .liouvillian import (compute_Nz_eq,
                          compute_base_liouvillians,
                          compute_liouvillian_free_precession,
                          get_Nz)

@lru_cache()
def make_calc_observable(time_t1=0.0, B1_offset=0.0, B1_frq=0.0, B1_inh=0.0, B1_inh_res=5,
                         carrier=0.0, ppm_to_rads=0.0, _id=None):
    """
    Factory to make "calc_observable" function to calculate the intensity in presence
    of exchange after a CEST block.

    Parameters
    ----------
    time_t1 : float
        Duration of the CW block.
    B1_offset : float
        Frequency offset of the applied B1 field in Hz.
    B1_frq : float
        Strength of the applied B1 field in Hz.
    B1_inh : float
        B1 field inhomogeneity in Hz.
    B1_inh_res : int
        Resolution to model B1 field inhomogeneity.
    carrier : float
        Carrier position in rad/s.
    ppm_to_rads : float
        Conversion factor from ppm to rad/s
    id : tuple
        Some type of identification for caching optimization

    Returns
    -------
    out : function
        Calculate intensity after the CEST block

    """

    liouvillians, weights = compute_base_liouvillians(B1_offset, B1_frq, B1_inh, B1_inh_res)

    @lru_cache(5)
    def _calc_observable(pb=0.0, pc=0.0, kex_ab=0.0, kex_bc=0.0, kex_ac=0.0,
                        dw_ab=0.0, dw_ac=0.0, r_Nz=1.5, r_Nxy=0.0,
                        dr_Nxy_ab=0.0, dr_Nxy_ac=0.0, cs=0.0):
        """
        Calculate the intensity in presence of exchange after a CEST block.

        Parameters
        ----------
        pb : float
            Fractional population of state B,
            0.0 for 0%, 1.0 for 100%
        pb : float
            Fractional population of state C,
            0.0 for 0%, 1.0 for 100%
        kex_ab : float
            Exchange rate between state A and B in /s.
        kex_bc : float
            Exchange rate between state B and C in /s.
        kex_ac : float
            Exchange rate between state A and C in /s.
        dw_ab : float
            Chemical shift difference between states A and B in rad/s.
        dw_ac : float
            Chemical shift difference between states A and C in rad/s.
        r_Nz : float
            Longitudinal relaxation rate of state {a,b} in /s.
        r_Nxy : float
            Transverse relaxation rate of state a in /s.
        dr_Nxy_ab : float
            Transverse relaxation rate difference between states a and c in /s.
        dr_Nxy_ac : float
            Transverse relaxation rate difference between states a and c in /s.
        cs : float
            Resonance position in rad/s.

        Returns
        -------
        out : float
            Intensity after the CEST block

        """

        if abs(B1_offset) >= 10000.0:

            return (1.0 - pb - pc)

        else:

            dw_ab *= ppm_to_rads
            dw_ac *= ppm_to_rads
            Ieq = compute_Nz_eq(pb, pc)
#             exchange_induced_shift, _ = correct_chemical_shift(pb=pb, kex=kex, dw=dw,
#                                                                r_Ixy=r_Nxy, dr_Ixy=dr_Nxy)
            exchange_induced_shift = 0.0  # TODO
            wg = (cs - carrier) * ppm_to_rads - exchange_induced_shift

            Ls = liouvillians + compute_liouvillian_free_precession(
                pb=pb, pc=pc, kex_ab=kex_ab, kex_bc=kex_bc, kex_ac=kex_ac,
                dw_ab=dw_ab, dw_ac=dw_ac, r_Nxy=r_Nxy, r_Nz=r_Nz, dr_Nxy_ab=dr_Nxy_ab,
                dr_Nxy_ac=dr_Nxy_ac, cs_offset=wg
            )

            propagator = sc.zeros_like(Ls[0])
            for L, weight in zip(Ls, weights):
                propagator += weight * expm(L * time_t1)
            propagator /= sum(weights)

            Ia, _Ib, _Ic = get_Nz(sc.dot(propagator, Ieq))

            return Ia

    def calc_observable(I0=0.0, **kwargs):
        """
        Calculate the intensity in presence of exchange after a CEST block.

        Parameters
        ----------
        I0 : float
            Initial intensity.

        Returns
        -------
        out : float
            Intensity after the CEST block

        """

        return I0 * _calc_observable(**kwargs)

    return calc_observable

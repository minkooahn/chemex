from __future__ import absolute_import

import numpy as np

from chemex.bases import ref

pi = np.pi


# Operator basis:
# {Ix, Iy, Iz, 2IxSz, 2IySz, 2IzSz}{a,b}

indexes = [0, 1, 2, 6, 7, 14, 15, 16, 17, 21, 22, 29]

mat_lambda_i_a = ref.mat_lambda_i_a[np.ix_(indexes, indexes)]
mat_lambda_i_b = ref.mat_lambda_i_b[np.ix_(indexes, indexes)]
mat_rho_i_a = ref.mat_rho_i_a[np.ix_(indexes, indexes)]
mat_rho_i_b = ref.mat_rho_i_b[np.ix_(indexes, indexes)]
mat_rhoa_i_a = ref.mat_rhoa_i_a[np.ix_(indexes, indexes)]
mat_rhoa_i_b = ref.mat_rhoa_i_b[np.ix_(indexes, indexes)]
mat_rho_is_a = ref.mat_rho_is_a[np.ix_(indexes, indexes)]
mat_rho_is_b = ref.mat_rho_is_b[np.ix_(indexes, indexes)]
mat_omega_i_a = ref.mat_omega_i_a[np.ix_(indexes, indexes)]
mat_omega_i_b = ref.mat_omega_i_b[np.ix_(indexes, indexes)]
mat_j_a = ref.mat_j_a[np.ix_(indexes, indexes)]
mat_j_b = ref.mat_j_b[np.ix_(indexes, indexes)]
mat_eta_i_a = ref.mat_eta_i_a[np.ix_(indexes, indexes)]
mat_eta_i_b = ref.mat_eta_i_b[np.ix_(indexes, indexes)]
mat_delta_i_a = ref.mat_delta_i_a[np.ix_(indexes, indexes)]
mat_delta_i_b = ref.mat_delta_i_b[np.ix_(indexes, indexes)]
mat_omega1x_i = ref.mat_omega1x_i[np.ix_(indexes, indexes)]
mat_omega1y_i = ref.mat_omega1y_i[np.ix_(indexes, indexes)]
mat_kab = ref.mat_kab[np.ix_(indexes, indexes)]
mat_kba = ref.mat_kba[np.ix_(indexes, indexes)]

p_180x_s = np.diag([1.0, 1.0, 1.0, -1.0, -1.0, -1.0,
                    1.0, 1.0, 1.0, -1.0, -1.0, -1.0])
p_180y_s = p_180x_s[:]


def compute_liouvillian(
        pb, kex_ab,
        lambda_i_a=0.0, rho_i_a=0.0, rhoa_i_a=0.0, eta_i_a=0.0, delta_i_a=0.0, omega_i_a=0.0,
        lambda_i_b=0.0, rho_i_b=0.0, rhoa_i_b=0.0, eta_i_b=0.0, delta_i_b=0.0, omega_i_b=0.0,
        rho_is_a=0.0, j_a=0.0,
        rho_is_b=0.0, j_b=0.0,
        omega1x_i=0.0, omega1y_i=0.0):
    """TODO: make docstringx
    """

    pa = 1.0 - pb
    kab, kba = kex_ab * np.asarray([pb, pa])

    liouvillian = (
        mat_lambda_i_a * lambda_i_a +
        mat_lambda_i_b * lambda_i_b +

        mat_rho_i_a * rho_i_a +
        mat_rho_i_b * rho_i_b +

        mat_rhoa_i_a * rhoa_i_a +
        mat_rhoa_i_b * rhoa_i_b +

        mat_eta_i_a * eta_i_a +
        mat_eta_i_b * eta_i_b +

        mat_delta_i_a * delta_i_a +
        mat_delta_i_b * delta_i_b +

        mat_omega_i_a * omega_i_a +
        mat_omega_i_b * omega_i_b +

        mat_rho_is_a * rho_is_a +
        mat_rho_is_b * rho_is_b +

        mat_j_a * j_a +
        mat_j_b * j_b +

        mat_omega1x_i * omega1x_i +
        mat_omega1y_i * omega1y_i +

        mat_kab * kab +
        mat_kba * kba
    )

    return liouvillian

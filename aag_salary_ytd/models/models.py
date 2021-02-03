# -*- coding: utf-8 -*-

from odoo import models, fields, api

class salary_ytd(models.Model):
    _name = 'aag_salary_ytd.aag_salary_ytd'
    _description = 'aag_salary_ytd.aag_salary_ytd'

    idno            = fields.Integer("IDNO")

    ## CURRENT MONTH ###
    m_year          = fields.Integer("Year", )
    m_curmm         = fields.Integer("Current Month", )

    # (1) Gaji/Pensiun atau JHT/THT 
    m_basic         = fields.Integer("Basic Salary", )
    m_tpk           = fields.Integer("TPK", )
    m_occup         = fields.Integer("Grade Allw", )
    m_functional    = fields.Integer("Functional Allw", )
    m_family        = fields.Integer("Family Allw", )
    m_perform       = fields.Integer("Performance Allw", )
    m_transport     = fields.Integer("Transport Allw", )
    m_presence      = fields.Integer("Presence Allw", )
    m_other         = fields.Integer("Other Income", )
    m_meal          = fields.Integer("Meal Allw", )
    m_shift         = fields.Integer("Shift Allw", )
    m_leave         = fields.Integer("Leave Replacement", )
    m_medical       = fields.Integer("Medical", )

    # (2) Tunjangan PPh
    m_pph21         = fields.Integer("Tunjangan PPh21", )

    # (3) Tunj Lainnya, Uang Lembur Dsb.
    m_overtime      = fields.Integer("Overime", )

    # (5) Premi Asuransi Yg dibayar Pemberi Kerja
    m_acccom        = fields.Integer("JKK Comp Allw", )
    m_dthcom        = fields.Integer("JKM Comp Allw", )
    m_bpjs_com      = fields.Integer("BPJS-Kes Com Allw", )

    # (7) Tantiem, Bonus, Gratifikasi, Jasa Produksi dan THR
    m_bonus         = fields.Integer("BONUS", )
    m_thr           = fields.Integer("THR", )

    # (10) Iuran Pensiun atau Iuran THT/JHT
    m_jhtemp        = fields.Integer("JHT Emp Deduction", )
    m_penemp        = fields.Integer("Pension Emp Deduction", )

    # Potongan Yang Tidak disertakan dalam Penghitungan PPh Pasal 21 Bulanan/Tahunan
    m_jhtcom        = fields.Integer("JHT Comp Allw", )
    m_pencom        = fields.Integer("Pension Comp Allw", )
    m_bpjs_emp      = fields.Integer("BPJS-Kes Emp Deduction", )
    m_spmicos       = fields.Integer("SPMI-COS", )
    m_spmimed       = fields.Integer("SPMI-Med", )
    m_spmi          = fields.Integer("SPMI-Deduction", )
    m_koperasi      = fields.Integer("Cooperation Deduction", )
    m_loan          = fields.Integer("Loan Deduction", )

    m_net           = fields.Integer("Net Salary", )
    m_reg_income    = fields.Integer("Regular Income", )
    m_irr_income    = fields.Integer("Irregular Income", )
    m_empl_pension  = fields.Integer("Employee Pension", )
    m_pphdtp        = fields.Integer("PPh21 DTP", )

    ### YEAR TO DATE UNTIL CURRENT MONTH ##
    y_year          = fields.Integer("Year", )
    y_strmm         = fields.Integer("Start Month", )
    y_endmm         = fields.Integer("End Month", )

    # (1) Gaji/Pensiun atau JHT/THT 
    y_basic         = fields.Integer("Basic Salary", )
    y_tpk           = fields.Integer("TPK", )
    y_occup         = fields.Integer("Grade Allw", )
    y_functional    = fields.Integer("Functional Allw", )
    y_family        = fields.Integer("Family Allw", )
    y_perform       = fields.Integer("Performance Allw", )
    y_transport     = fields.Integer("Transport Allw", )
    y_presence      = fields.Integer("Presence Allw", )
    y_other         = fields.Integer("Other Income", )
    y_meal          = fields.Integer("Meal Allw", )
    y_shift         = fields.Integer("Shift Allw", )
    y_leave         = fields.Integer("Leave Replacement", )
    y_medical       = fields.Integer("Medical", )

    # (2) Tunjangan PPh
    y_pph21         = fields.Integer("Tunjangan PPh21", )

    # (3) Tunj Lainnya, Uang Lembur Dsb.
    y_overtime      = fields.Integer("Overime", )

    # (5) Premi Asuransi Yg dibayar Pemberi Kerja
    y_acccom        = fields.Integer("JKK Comp Allw", )
    y_dthcom        = fields.Integer("JKM Comp Allw", )
    y_bpjs_com      = fields.Integer("BPJS-Kes Com Allw", )

    # (7) Tantiem, Bonus, Gratifikasi, Jasa Produksi dan THR
    y_bonus         = fields.Integer("BONUS", )
    y_thr           = fields.Integer("THR", )

    # (10) Iuran Pensiun atau Iuran THT/JHT
    y_jhtemp        = fields.Integer("JHT Emp Deduction", )
    y_penemp        = fields.Integer("Pension Emp Deduction", )

    # Potongan Yang Tidak disertakan dalam Penghitungan PPh Pasal 21 Bulanan/Tahunan
    y_jhtcom        = fields.Integer("JHT Comp Allw", )
    y_pencom        = fields.Integer("Pension Comp Allw", )
    y_bpjs_emp      = fields.Integer("BPJS-Kes Emp Deduction", )
    y_spmicos       = fields.Integer("SPMI-COS", )
    y_spmimed       = fields.Integer("SPMI-Med", )
    y_spmi          = fields.Integer("SPMI-Deduction", )
    y_koperasi      = fields.Integer("Cooperation Deduction", )
    y_loan          = fields.Integer("Loan Deduction", )

    y_net           = fields.Integer("Net Salary", )
    y_reg_income    = fields.Integer("Regular Income", )
    y_irr_income    = fields.Integer("Irregular Income", )
    y_empl_pension  = fields.Integer("Employee Pension", )
    y_pphdtp        = fields.Integer("PPh21 DTP", )

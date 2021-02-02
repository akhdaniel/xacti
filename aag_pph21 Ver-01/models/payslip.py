from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)



class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    ptkp = fields.Integer("PTKP", related="employee_id.ptkp_id.nominal")
    bruto = fields.Integer("Bruto", )
    bjab = fields.Integer("Biaya Jabatan", )
    netto = fields.Integer("Netto", )
    pkp = fields.Integer("PKP", )
    pph21_thn = fields.Integer("PPH21 Setahun", )
    pph21_paid = fields.Integer("PPh21 Paid")
      
    tunj_pph = fields.Integer("Tunjangan PPH")
    pot_pph = fields.Integer("Pot PPH")

    pph21med = fields.Integer("PPh21 Medical")
    pph21ovt = fields.Integer("PPh21 Overtime")
    pph21thr = fields.Integer("PPh21 THR")
    pph21bon = fields.Integer("PPh21 Bonus")
    pph21irr = fields.Integer("PPh21 Irregular")
    pph21reg = fields.Integer("PPh21 Regular")

    basic = fields.Integer("Basic Salary", )
    i_basic = fields.Integer("Basic Salary Add", )
    i_tpk = fields.Integer("TPK", )
    i_occup = fields.Integer("Grade Allw", )
    i_functional = fields.Integer("Functional Allw", )
    i_family = fields.Integer("Family Allw", )
    i_perform = fields.Integer("Performance Allw", )
    i_transport = fields.Integer("Transport Allw", )
    i_presence = fields.Integer("Presence Allw", )
    i_other = fields.Integer("Other Income", )
    i_meal = fields.Integer("Meal Allw", )
    i_shift = fields.Integer("Shift Allw", )
    i_leave = fields.Integer("Leave Replacement", )
    i_overtime = fields.Integer("Overime", )
    i_medical = fields.Integer("Medical", )
    i_bpjs_com = fields.Integer("BPJS-Kes Com Allw", )
    i_jhtcom = fields.Integer("JHT Comp Allw", )
    i_acccom = fields.Integer("JKK Comp Allw", )
    i_dthcom = fields.Integer("JKM Comp Allw", )
    i_pencom = fields.Integer("Pension Comp Allw", )
    i_pphdtp = fields.Integer("PPh21 DTP", )
    i_pph21 = fields.Integer("PPh21", )
    i_thr = fields.Integer("THR", )
    i_bonus = fields.Integer("BONUS", )

    t_income = fields.Integer("Total Income", )

    d_basic = fields.Integer("Basic Salary. Deduction", )
    d_transport = fields.Integer("Transport Deduction", )
    d_spmicos = fields.Integer("SPMI-COS", )
    d_spmimed = fields.Integer("SPMI-Med", )
    d_spmi = fields.Integer("SPMI-Deduction", )
    d_jhtemp = fields.Integer("JHT Emp Deduction", )
    d_jhtcom = fields.Integer("JHT Comp Deduction", )
    d_acccom = fields.Integer("JKK Comp Deduction", )
    d_dthcom = fields.Integer("JKM Comp Deduction", )
    d_penemp = fields.Integer("Pension Emp Deduction", )
    d_pencom = fields.Integer("Pension Comp Deduction", )
    d_bpjs_emp = fields.Integer("BPJS-Kes Emp Deduction", )
    d_bpjs_com = fields.Integer("BPJS-Kes Com Deduction", )
    d_koperasi = fields.Integer("Cooperation Deduction", )
    d_loan = fields.Integer("Loan Deduction", )
    d_other = fields.Integer("Other Deduction", )
    d_medical = fields.Integer("Medical", )
    d_pph21 = fields.Integer("PPh21 Deduction", )

    t_deduction = fields.Integer("Total Deduction", )

    net = fields.Integer("Net Salary", )

    prev_leave_bal = fields.Float("Prev Leave Balance")
    curr_leave_use = fields.Float("Curr Leave Usage")
    curr_leave_bal = fields.Float("Curr Leave Balance")
    prev_med_bal = fields.Integer("Prev Medical Balance")
    curr_med_use = fields.Integer("Curr Medical Usage")
    curr_med_bal = fields.Integer("Curr Medical Balance")

    def compute_sheet(self):
        
        res = super(hr_payslip, self).compute_sheet() 

        for payslip in self:
            # read hr_payslip_line
            # payslip._read_payslip_line(medical=True, overtime=True, thr=True, bonus=True)
            # initialize_fields
            # self.ptkp = 0
            # self.bruto = 0
            # self.bjab = 0
            # self.netto = 0
            # self.pkp = 0
            # self.pph21_thn = 0
            # self.pph21_paid = 0
            # self.tunj_pph = 0
            # self.pot_pph = 0
            # self.pph21med = 0
            # self.pph21ovt = 0
            # self.pph21thr = 0
            # self.pph21bon = 0
            # self.pph21irr = 0
            # self.pph21reg = 0

            # self.basic = 0
            # self.i_basic = 0
            # self.i_tpk = 0
            # self.i_occup = 0
            # self.i_presence = 0
            # self.i_family = 0
            # self.i_functional = 0
            # self.i_transport = 0
            # self.i_perform = 0
            # self.i_meal = 0
            # self.i_shift = 0
            # self.i_leave = 0
            # self.i_jhtcom = 0
            # self.i_acccom = 0
            # self.i_dthcom = 0
            # self.i_pencom = 0
            # self.i_bpjs_com = 0
            # self.i_overtime = 0
            # self.i_medical = 0
            # self.i_pphdtp = 0
            # self.i_pph21 = 0
            # self.i_thr = 0
            # self.i_bonus = 0
            # self.i_other = 0
            # self.t_income = 0

            # self.d_basic = 0
            # self.d_transport = 0
            # self.d_spmicos = 0
            # self.d_spmimed = 0
            # self.d_spmi = 0
            # self.d_jhtemp = 0
            # self.d_jhtcom = 0
            # self.d_acccom = 0
            # self.d_dthcom = 0
            # self.d_penemp = 0
            # self.d_pencom = 0
            # self.d_bpjs_emp = 0
            # self.d_bpjs_com = 0
            # self.d_koperasi = 0
            # self.d_loan = 0
            # self.d_other = 0
            # self.d_medical = 0
            # self.d_pph21 = 0
            # self.t_deduction = 0

            # self.net = 0

            # self.prev_leave_bal = 0
            # self.curr_leave_use = 0
            # self.curr_leave_bal = 0

            # self.prev_med_bal = 0
            # self.curr_med_use = 0
            # self.curr_med_bal = 0

            payslip._read_payslip_line()
            _logger.info("--- compute sheet --- %s %s", payslip.line_ids,  )

        return res 

    # def _read_payslip_line(self, medical=True, overtime=True, thr=True, bonus=True):
    def _read_payslip_line(self):
        for line in self.line_ids:
            if line.code=='BASIC':
                self.basic=line.amount
            if line.code=='I_BASIC':
                self.i_basic=line.amount
            if line.code=='I_TPK':
                self.i_tpk=line.amount
            if line.code=='I_OCCUP':
                self.i_occup=line.amount
            if line.code=='I_FUNCTIONAL':
                self.i_functional=line.amount
            if line.code=='I_FAMILY':
                self.i_family=line.amount
            if line.code=='I_PERFORM':
                self.i_perform=line.amount
            if line.code=='I_TRANSPORT':
                self.i_transport=line.amount
            if line.code=='I_PRESENCE':
                self.i_presence=line.amount
            if line.code=='I_MEAL':
                self.i_meal=line.amount
            if line.code=='I_SHIFT':
                self.i_shift=line.amount
            if line.code=='I_LEAVE':
                self.i_leave=line.amount
            if line.code=='I_OTHER':
                self.i_other=line.amount
            if line.code=='I_JHTCOM':
                self.i_jhtcom=line.amount
            if line.code=='I_ACCCOM':
                self.i_acccom=line.amount
            if line.code=='I_DTHCOM':
                self.i_dthcom=line.amount
            if line.code=='I_PENCOM':
                self.i_pencom=line.amount
            if line.code=='I_BPJSKES_COM':
                self.i_bpjs_com=line.amount
            if line.code=='I_OVERTIME':
                self.i_overtime=line.amount
            if line.code=='I_MEDICAL':
                self.i_medical=line.amount
            if line.code=='I_PPH_DTP':
                self.i_pphdtp=line.amount
            if line.code=='I_PPH21':
                self.i_pph21=line.amount
            if line.code=='I_THR':
                self.i_thr=line.amount
            if line.code=='I_BONUS':
                self.i_bonus=line.amount
            if line.code=='GROSS':
                self.t_income = line.amount

    # === READ DEDUCTION ====
            if line.code=='I_BASIC':
                self.d_basic = line.amount
            if line.code=='D_TRANSPORT':
                self.d_transport = line.amount
            if line.code=='D_SPMICOS':
                self.d_spmicos = line.amount
            if line.code=='D_SPMIMED':
                self.d_spmimed = line.amount
            if line.code=='D_SPMI':
                self.d_spmi = line.amount
            if line.code=='D_JHTEMP':
                self.d_jhtemp = line.amount
            if line.code=='D_JHTCOM':
                self.d_jhtcom = line.amount
            if line.code=='D_ACCCOM':
                self.d_acccom = line.amount
            if line.code=='D_DTHCOM':
                self.d_dthcom = line.amount
            if line.code=='D_PENEMP':
                self.d_penemp = line.amount
            if line.code=='D_PENCOM':
                self.d_pencom = line.amount
            if line.code=='D_BPJSKES_EMP':
                self.d_bpjs_emp = line.amount
            if line.code=='D_BPJSKES_COM':
                self.d_bpjs_com = line.amount
            if line.code=='D_KOPERASI':
                self.d_koperasi = line.amount
            if line.code=='D_LOAN':
                self.d_loan = line.amount
            if line.code=='D_OTHER':
                self.d_other = line.amount
            if line.code=='D_MEDICAL':
                self.d_medical = line.amount
            if line.code=='D_PPH21':
                self.d_pph21 = line.amount
            if line.code=='TDED':
                self.t_deduction = line.amount

    # === READ NET AND BALANCE  ====
            if line.code=='NET':
                self.net = line.amount

            if line.code=='I_PREV_LEAVE_BAL':
                self.prev_leave_bal = line.amount
            if line.code=='I_LEAVE_USE':
                self.curr_leave_use = line.amount
            if line.code=='I_LEAVE_BAL':
                self.curr_leave_bal = line.amount

            if line.code=='I_PREV_MEDICAL_BAL':
                self.prev_med_bal = line.amount
            if line.code=='I_MEDICAL_USE':
                self.curr_med_use = line.amount
            if line.code=='I_MED_ALW_BAL':
                self.curr_med_bal = line.amount


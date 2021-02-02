from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)



class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    x_idno = fields.Integer("IDNO", related="employee_id.x_idno")

    #   *****  ATURAN PENGHITUNGAN Pajak Penghasilan Ps.21  *****
    #
    #   A. Nilai Pajak Dihitung atas Penghasilan Teratur yg disetahunkan + Penghasilan Tak Teratur (tidak disetahunkan)
    #       1. Penghasilan Teratur. (Gaji Pokok dan Tunjangan Tetap + Komponen selain Point 2.)
    #       2. Penghasilan Tidak Teratur.
    #           a. THR
    #           b. Bonus
    #           c. Lembur
    #           d. Penggantian Medical
    #
    #   B. Nilai Pajak s/d bulan berjalan(n) adalah hasil pada point (A) dibagi secara proporsional s/d bulan berjalan(n). (Nilai pajak n bulan)
    #   C. Nilai pajak yg harus dibayar untuk bulan berjalan adalah Nilai pada point (B) dikurangi dengan pajak yg sudah dibayar s/d bulan n-1.
    # 

    ptkp = fields.Integer("PTKP", related="employee_id.ptkp_id.nominal")
    bruto = fields.Integer("Bruto", )
    bjab = fields.Integer("Biaya Jabatan", )
    netto = fields.Integer("Netto", )
    pkp = fields.Integer("PKP", )
    pph21_thn = fields.Integer("PPH21 Setahun", )
    pph21_paid = fields.Integer("PPh21 Paid")
      
    tunj_pph = fields.Integer("Tunjangan PPH")
    pot_pph = fields.Integer("Pot PPH")

    pph21med_yr = fields.Integer("PPh21 Medical Yr")
    pph21ovt_yr = fields.Integer("PPh21 Overtime Yr")
    pph21thr_yr = fields.Integer("PPh21 THR Yr")
    pph21bon_yr = fields.Integer("PPh21 Bonus Yr")
    pph21irr_yr = fields.Integer("PPh21 Irregular Yr")
    pph21reg_yr = fields.Integer("PPh21 Regular Yr")

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

    m_basic = fields.Integer("Basic Salary", )
    m_tpk = fields.Integer("TPK", )
    m_occup = fields.Integer("Grade Allw", )
    m_functional = fields.Integer("Functional Allw", )
    m_family = fields.Integer("Family Allw", )
    m_perform = fields.Integer("Performance Allw", )
    m_transport = fields.Integer("Transport Allw", )
    m_presence = fields.Integer("Presence Allw", )
    m_other = fields.Integer("Other Income", )
    m_meal = fields.Integer("Meal Allw", )
    m_shift = fields.Integer("Shift Allw", )
    m_leave = fields.Integer("Leave Replacement", )
    m_overtime = fields.Integer("Overime", )
    m_medical = fields.Integer("Medical", )
    m_bpjs_com = fields.Integer("BPJS-Kes Com Allw", )
    m_jhtcom = fields.Integer("JHT Comp Allw", )
    m_acccom = fields.Integer("JKK Comp Allw", )
    m_dthcom = fields.Integer("JKM Comp Allw", )
    m_pencom = fields.Integer("Pension Comp Allw", )
    m_pphdtp = fields.Integer("PPh21 DTP", )
    m_pph21 = fields.Integer("PPh21", )
    m_thr = fields.Integer("THR", )
    m_bonus = fields.Integer("BONUS", )

    m_spmicos = fields.Integer("SPMI-COS", )
    m_spmimed = fields.Integer("SPMI-Med", )
    m_spmi = fields.Integer("SPMI-Deduction", )
    m_jhtemp = fields.Integer("JHT Emp Deduction", )
    m_penemp = fields.Integer("Pension Emp Deduction", )
    m_bpjs_emp = fields.Integer("BPJS-Kes Emp Deduction", )
    m_koperasi = fields.Integer("Cooperation Deduction", )
    m_loan = fields.Integer("Loan Deduction", )

    m_net = fields.Integer("Net Salary", )

    m_reg_income = fields.Integer("Regular Income", )
    m_irr_income = fields.Integer("Irregular Income", )
    m_empl_pension = fields.Integer("Employee Pension", )


    def compute_sheet(self):
        
        res = super(hr_payslip, self).compute_sheet() 

        for payslip in self:
            payslip._read_payslip_line()
            # _logger.info("--- compute sheet --- %s %s", payslip.line_ids,  )
            payslip.m_reg_income = payslip.m_basic+payslip.m_tpk+payslip.m_transport+payslip.m_presence+payslip.m_occup+payslip.m_family+payslip.m_functional+payslip.m_perform+payslip.m_other+payslip.m_shift+payslip.tunj_pph+payslip.m_jhtcom+payslip.m_acccom+payslip.m_dthcom+payslip.m_bpjs_com
            payslip.m_irr_income = payslip.m_overtime + payslip.m_medical + payslip.m_thr + payslip.m_bonus
            payslip.m_empl_pension = payslip.m_jhtemp + payslip.m_penemp

            payslip._calculate_pph(medical=True, overtime=True, thr=True, bonus=True)
            i=0
            selisih = round(payslip.pot_pph - payslip.tunj_pph)
            while selisih != 0:
            #    _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
                payslip.tunj_pph = payslip.pot_pph
                payslip._calculate_pph(medical=True, overtime=True, thr=True, bonus=True) 
                selisih = round(payslip.pot_pph - payslip.tunj_pph)
            #    i+=1

            pph_all = payslip.pot_pph 

            # cari selisih medical
            payslip.pph21med = 0 
            #payslip.cari_selisih('pph21med', pph_all)
        
            # cari selisih overtime
            payslip.pph21ovt = 0 
            #payslip.cari_selisih('pph21ovt', pph_all)
        
            # cari selisih THR
            payslip.pph21thr = 0 
            #payslip.cari_selisih('pph21thr', pph_all)
        
            # cari selisih bonus 
            payslip.pph21bon = 0 
            #payslip.cari_selisih('pph21bon', pph_all)
        
            irr_acc = payslip.find_irr_acc()        
            #payslip.pph21ovt = payslip.pph21ovt - (irr_acc['x_pph_accovt'] if irr_acc else 0)
            #payslip.pph21med = payslip.pph21med - (irr_acc['x_pph_accmed'] if irr_acc else 0)
            #payslip.pph21thr = payslip.pph21thr - (irr_acc['x_pph_accthr'] if irr_acc else 0)
            #payslip.pph21bon = payslip.pph21bon - (irr_acc['x_pph_accbon'] if irr_acc else 0)

            payslip.pot_pph = pph_all - (irr_acc['x_pph_accgrs']+irr_acc['x_pph_accovt']+irr_acc['x_pph_accmed']+irr_acc['x_pph_accthr']+irr_acc['x_pph_accbon'] if irr_acc else 0)
            payslip.tunj_pph = pph_all - (irr_acc['x_pph_accgrs']+irr_acc['x_pph_accovt']+irr_acc['x_pph_accmed']+irr_acc['x_pph_accthr']+irr_acc['x_pph_accbon'] if irr_acc else 0)

            payslip.pph21irr = payslip.pph21ovt + payslip.pph21med + payslip.pph21thr + payslip.pph21bon
            payslip.pph21reg = payslip.pot_pph - payslip.pph21irr

        return res 

    def _read_payslip_line(self):
        for line in self.line_ids:

            if line.code == 'BASIC':
                self.basic = line.amount
                self.m_basic = self.basic
            elif line.code=='I_BASIC':
                self.i_basic = line.amount
                self.m_basic += self.i_basic
            elif line.code=='I_TPK':
                self.i_tpk = line.amount
                self.m_tpk = line.amount
            elif line.code=='I_OCCUP':
                self.i_occup = line.amount
                self.m_occup = line.amount
            elif line.code=='I_FUNCTIONAL':
                self.i_functional = line.amount
                self.m_functional = line.amount
            elif line.code=='I_FAMILY':
                self.i_family = line.amount
                self.m_family = line.amount
            elif line.code=='I_PERFORM':
                self.i_perform = line.amount
                self.m_perform = line.amount
            elif line.code=='I_TRANSPORT':
                self.i_transport = line.amount
                self.m_transport = line.amount
            elif line.code=='I_PRESENCE':
                self.i_presence = line.amount
                self.m_presence = line.amount
            elif line.code=='I_MEAL':
                self.i_meal=line.amount
                self.m_meal=line.amount
            elif line.code=='I_SHIFT':
                self.i_shift=line.amount
                self.m_shift=line.amount
            elif line.code=='I_LEAVE':
                self.i_leave=line.amount
                self.m_leave=line.amount
            elif line.code=='I_OTHER':
                self.i_other=line.amount
                self.m_other=line.amount
            elif line.code=='I_JHTCOM':
                self.i_jhtcom=line.amount
                self.m_jhtcom=line.amount
            elif line.code=='I_ACCCOM':
                self.i_acccom=line.amount
                self.m_acccom=line.amount
            elif line.code=='I_DTHCOM':
                self.i_dthcom=line.amount
                self.m_dthcom=line.amount
            elif line.code=='I_PENCOM':
                self.i_pencom=line.amount
                self.m_pencom=line.amount
            elif line.code=='I_BPJSKES_COM':
                self.i_bpjs_com=line.amount
                self.m_bpjs_com=line.amount
            elif line.code=='I_OVERTIME':
                self.i_overtime=line.amount
                self.m_overtime=line.amount
            elif line.code=='I_MEDICAL':
                self.i_medical=line.amount
                self.m_medical=line.amount
            elif line.code=='I_PPH_DTP':
                self.i_pphdtp=line.amount
                self.m_pphdtp=line.amount
            elif line.code=='I_PPH21':
                self.i_pph21=line.amount
                self.m_pph21=line.amount
            elif line.code=='I_THR':
                self.i_thr=line.amount
                self.m_thr=line.amount
            elif line.code=='I_BONUS':
                self.i_bonus=line.amount
                self.m_bonus=line.amount
            elif line.code=='GROSS':
                self.t_income = line.amount

    # # === READ DEDUCTION ====
            elif line.code=='D_BASIC':
                self.d_basic = line.amount
                self.m_basic -= self.d_basic
            elif line.code=='D_TRANSPORT':
                self.d_transport = line.amount
                self.m_transport -= line.amount
            elif line.code=='D_SPMICOS':
                self.d_spmicos = line.amount
                self.m_spmicos = line.amount
            elif line.code=='D_SPMIMED':
                self.d_spmimed = line.amount
                self.m_spmimed = line.amount
            elif line.code=='D_SPMI':
                self.d_spmi = line.amount
                self.m_spmi = line.amount
            elif line.code=='D_JHTEMP':
                self.d_jhtemp = line.amount
                self.m_jhtemp = line.amount
            elif line.code=='D_JHTCOM':
                self.d_jhtcom = line.amount
            elif line.code=='D_ACCCOM':
                self.d_acccom = line.amount
            elif line.code=='D_DTHCOM':
                self.d_dthcom = line.amount
            elif line.code=='D_PENEMP':
                self.d_penemp = line.amount
                self.m_penemp = line.amount
            elif line.code=='D_PENCOM':
                self.d_pencom = line.amount
            elif line.code=='D_BPJSKES_EMP':
                self.d_bpjs_emp = line.amount
                self.m_bpjs_emp = line.amount
            elif line.code=='D_BPJSKES_COM':
                self.d_bpjs_com = line.amount
            elif line.code=='D_KOPERASI':
                self.d_koperasi = line.amount
                self.m_koperasi = line.amount
            elif line.code=='D_LOAN':
                self.d_loan = line.amount
                self.m_loan = line.amount
            elif line.code=='D_OTHER':
                self.d_other = line.amount
                self.m_other -= line.amount
            elif line.code=='D_MEDICAL':
                self.d_medical = line.amount
                self.m_medical -= line.amount
            elif line.code=='D_PPH21':
                self.d_pph21 = line.amount
            elif line.code=='TDED':
                self.t_deduction = line.amount

    # === READ NET AND BALANCE  ====
            elif line.code=='NET':
                self.net = line.amount
                self.m_net = line.amount

            elif line.code=='I_PREV_LEAVE_BAL':
                self.prev_leave_bal = line.amount
            elif line.code=='I_LEAVE_USE':
                self.curr_leave_use = line.amount
            elif line.code=='I_LEAVE_BAL':
                self.curr_leave_bal = line.amount

            elif line.code=='I_PREV_MEDICAL_BAL':
                self.prev_med_bal = line.amount
            elif line.code=='I_MEDICAL_USE':
                self.curr_med_use = line.amount
            elif line.code=='I_MED_ALW_BAL':
                self.curr_med_bal = line.amount

    def cari_selisih(self, komponen, pph_all):

        if komponen == 'pph21med':
            medical = False
            overtime = True
            thr = True
            bonus = True
        elif komponen == 'pph21ovt':
            medical = True
            overtime = False
            thr = True
            bonus = True
        elif komponen == 'pph21thr':
            medical = True
            overtime = True
            thr = False
            bonus = True
        elif komponen == 'pph21bon':
            medical = True
            overtime = True
            thr = True
            bonus = False

    #*************
        self._calculate_pph(medical=medical, overtime=overtime, thr=thr, bonus=bonus)
        
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            # _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(medical=medical, overtime=overtime, thr=thr, bonus=bonus)
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1
        # self.pph21med = self.pph21med  - self.pot_pph
        setattr(self, komponen, pph_all - self.pot_pph)

    def _calculate_pph(self, medical=True, overtime=True, thr=True, bonus=True):
    #        _logger.info("--- awal bruto = %s", self.bruto)
    #        _logger.info("--- new tunj_pph = %s", self.tunj_pph)

        akumulasi = self.cari_akumulasi(medical=medical, overtime=overtime, thr=thr, bonus=bonus )
        # curr_reg_income = self.m_basic+self.m_tpk+self.m_transport+self.m_presence+self.m_occup+self.m_family+self.m_functional+self.m_perform+self.m_other+self.m_shift+self.tunj_pph+self.m_jhtcom+self.m_acccom+self.m_dthcom+self.m_bpjs_com
        total_reg_income_accum = self.m_reg_income + (akumulasi['x_accgrs'] if akumulasi else 0)
        # curr_irr_income = self.m_overtime + self.m_medical + self.m_thr + self.m_bonus

        # m_irr_income modified based on "cari selisih pajak/pajak irregular income???????????

        curr_irr_income = self.m_irr_income
        if medical == False:
            curr_irr_income = self.m_irr_income - self.m_medical
        elif overtime == False:
            curr_irr_income = self.m_irr_income - self.m_overtime
        elif thr == False:
            curr_irr_income = self.m_irr_income - self.m_thr
        elif bonus == False:
            curr_irr_income = self.m_irr_income - self.m_bonus

        # total_irr_income_accum =  self.m_irr_income + (akumulasi['x_accovt']+akumulasi['x_accmed']+akumulasi['x_accthr']+akumulasi['x_accbon'] if akumulasi else 0)
        total_irr_income_accum =  curr_irr_income + (akumulasi['x_accovt']+akumulasi['x_accmed']+akumulasi['x_accthr']+akumulasi['x_accbon'] if akumulasi else 0)


        # temporary set total_irr_income_accum = 0 (calculate pph for regular income only)
        # total_irr_income_accum = 0

        total_empl_pension_accum =  self.m_empl_pension + (akumulasi['x_accjht2']+akumulasi['x_accpen1'] if akumulasi else 0)
        
        # self.bruto = (curr_reg_income * 12) + curr_irr_income 
        # ganti kalkulasi menjadi: 
        bulan_berjalan = self.date_to.month 
        self.bruto = ( total_reg_income_accum * 12 )/bulan_berjalan + total_irr_income_accum

        # _logger.info("--- new bruto = %s", self.bruto)
        self.env.cr.commit()

        self.bjab = min(0.05 * self.bruto , 6000000)	
        self.netto = self.bruto-self.bjab-((total_empl_pension_accum * 12)/bulan_berjalan)
        # self.netto = self.bruto-self.bjab-total_empl_pension_accum 			
        self.pkp = self.netto - self.ptkp if self.netto - self.ptkp >0 else 0

        # Karyawan kontrak di-set pph21 = 0
        if self.contract_id.employee_id.x_empsts=='C':
            self.pph21_thn = 0
        else:
            self.pph21_thn = round(self.get_pph21_setahun(), 0)

        pph_sdh_dibayar = akumulasi['x_pph_accgrs']+akumulasi['x_pph_accovt']+akumulasi['x_pph_accmed']+akumulasi['x_pph_accthr']+akumulasi['x_pph_accbon'] if akumulasi else 0
        self.pph21_paid = pph_sdh_dibayar

        # temporary set pph_paid regular income only
        # self.pph21_paid = akumulasi['x_pph_accgrs']

        # untuk selisih irrregular income
        # pengurangan sudah dibayar (pph_sdh_dibayar) dihitung saat sudah didapat selisihnya
        # self.pot_pph = round(self.pph21_thn/12 * bulan_berjalan - pph_sdh_dibayar, 0)
        
        self.pot_pph = round(self.pph21_thn/12 * bulan_berjalan, 0)
        # bisa minus, kalau minus -> pot_pph=0.. min(pot_pph, 0 )
            # rec.pot_pph = max(rec.pot_pph, 0)
    
    def get_pph21_setahun(self):
        sisa_pkp = self.pkp 
        pph21 = 0 
        range = self.contract_id.company_id.pkp_ids[0]
        if self.pkp > range.maximum:
            pph21 += range.maximum * range.rate / 100 
            sisa_pkp = self.pkp - range.maximum
            range = self.contract_id.company_id.pkp_ids[1]
            if sisa_pkp <= (range.maximum-range.minimum+1):
                pph21 += sisa_pkp*range.rate/100 
            else:
                pph21 += (range.maximum-range.minimum+1) * range.rate / 100
                sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                range = self.contract_id.company_id.pkp_ids[2]
                if sisa_pkp <= (range.maximum-range.minimum+1):
                    pph21 += sisa_pkp*range.rate/100
                else:
                    pph21 += (range.maximum-range.minimum+1)*range.rate/100
                    sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                    range = self.contract_id.company_id.pkp_ids[3]
                    pph21 += sisa_pkp*range.rate/100
        else:
            pph21 = self.pkp*range.rate/100        
        return pph21

    # def cari_akumulasi(self, medical=True, overtime=True, thr=True, bonus=True):
    def cari_akumulasi(self, medical=True, overtime=True, thr=True, bonus=True):
    
        cr = self.env.cr
        sql = "select * from aag_pph_accumulation_aag_pph_accumulation where idno=%s"
        # cr.execute(sql, (self.employee_id.x_idno,))
        cr.execute(sql, (self.contract_id.employee_id.x_idno,))

        akumulasi = cr.dictfetchone()

        if not medical:
            akumulasi['x_accmed'] = 0
        if not overtime:
            akumulasi['x_accovt'] = 0
        if not thr:
            akumulasi['x_accthr'] = 0
        if not bonus:
            akumulasi['x_accbon'] = 0

        return akumulasi

    def find_irr_acc(self):
        cr = self.env.cr
        sql = "select * from aag_pph_accumulation_aag_pph_accumulation where idno=%s"
        cr.execute(sql, (self.employee_id.x_idno,))
        irr_acc = cr.dictfetchone()

        return irr_acc    




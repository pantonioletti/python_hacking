#coding=ISO_8859-1
'''
Created on Aug 12, 2010

@author: pantonio
'''
from xml.dom.minidom import parseString

class rotation_balance:
    def __init__(self, id, weeks, org_id):
        self.id = id
        self.weeks = weeks
        self.org_id = org_id
        self.min_week = 0
        self.max_week = 0
        self.week_bal = dict()
        for i in range(self.weeks):
            self.week_bal[i+1]=0
    def set_week_balance(self, week, count):
        self.week_bal[week] = count
    def evaluate_balance(self):
        min = 100
        max = 0
        self.min_week = 0
        self.max_week = 0
        for key in self.week_bal.keys():
            if self.week_bal[key] < min:
                min = self.week_bal[key]
                self.min_week = key
            if self.week_bal[key] > max:
                max = self.week_bal[key]
                self.max_week = key
        eval = max - min > 1
        
        if eval:
            return self.max_week
        else:
            return -1
    def rebalance(self,week):
        self.week_bal[week] -=1
        self.week_bal[self.min_week] += 1
        return self.min_week - week

class rotation:
    def __init__(self, id, weeks):
        self.id = id
        self.weeks = weeks
        self.avail = dict()
        for next_w in range(self.weeks):
            self.avail[next_w + 1] = "0000000"

def get_emps_to_move(conn):
    
    sql = "select emps.e_id, emps.startd, emps.endd, emps.rtype from ( "
    sql += "select sbe.emp_id e_id, sbe.start_sdate startd, sbe.end_sdate endd, 'B' rtype "
    sql += "from sched_build_emp sbe "
    sql += "where sbe.start_sdate = '20100830' "
    sql += "and sbe.emp_id not in (select sbe2.emp_id  "
    sql += "                      from sched_build_emp sbe2 "
    sql += "                      where sbe2.start_sdate in ('20100802', '20100809', '20100816', '20100823')) "
    sql += "union "
    sql += "select eop.emp_id e_id, to_char(eop.eff_date,'yyyymmdd') startd, to_char(eop.end_date,'yyyymmdd') endd, 'P' rtype "
    sql += "from emp_org_position eop "
    sql += "where eop.eff_date >= to_date('20100830','yyyymmdd') "
    sql += "and (eop.end_date is null or eop.end_date > to_date('20100905','yyyymmdd')) "
    sql += "union "
    sql += "select esp.emp_id e_id, esp.eff_sdate startd, esp.end_sdate endd, 'S' rtype "
    sql += "from emp_sched_plan esp "
    sql += "where esp.eff_sdate >= '20100830' "
    sql += "and (esp.end_sdate is null or esp.end_sdate > '20100905') "
    sql += ") emps "
    sql += "order by emps.e_id "    

    cursor = conn.cursor()
    cursor.execute(sql)
    emps = cursor.fetchall()
    cursor.close()
    
    d_emps = dict()
    if len(emps) > 0:
        for next_emp in emps:
            if next_emp[0] not in d_emps:
                d_emps[next_emp[0]]=list()
            d_emps[next_emp[0]].append(next_emp)
    return d_emps

def get_rotation_bal(conn):
    sql = "select rot.sched_rotation_id, rot.org_entry_id, rot.semana, rot.number_of_weeks, count(*) from "
    sql += "(select sr.sched_rotation_id, oe.org_entry_id,sr.number_of_weeks,   "
    sql += "           mod((trunc(to_date('30-08-2010', 'dd-mm-yyyy'), 'd') - "
    sql += "           trunc(to_date(esr.eff_sdate, 'yyyymmdd'), 'd')) / 7 + "
    sql += "           esr.week_counter, "
    sql += "           sr.number_of_weeks) + 1 semana "
    sql += "from sched_rotation sr,  "
    sql += "     org_sched_rotation osr,  "
    sql += "     org_entry oe,  "
    sql += "     emp_sched_rotation esr,  "
    sql += "     v_emp e,  "
    sql += "     emp_org_position eop,  "
    sql += "     org_position op "
    sql += "where osr.sched_rotation_id = sr.sched_rotation_id "
    sql += "and esr.sched_rotation_id = sr.sched_rotation_id "
    sql += "and oe.org_entry_id = osr.org_entry_id "
    sql += "and op.org_entry_id = osr.org_entry_id "
    sql += "and eop.org_position_id = op.org_position_id "
    sql += "and eop.emp_id = esr.emp_id "
    sql += "and e.emp_id = esr.emp_id "
    sql += "and eop.eff_date < to_date('20100906','yyyymmdd') "
    sql += "and (eop.end_date is null or eop.end_date > to_date('20100830','yyyymmdd')) "
    sql += "and esr.eff_sdate < '20100906' "
    sql += "and (esr.end_sdate is null or esr.end_sdate >= '20100830') "
    sql += "and (sr.sched_rotation_name, oe.org_entry_cd) in "
    sql += "( "
    sql += "('FT Ahumada','112-305'),('FT Rotacion 5x2','1201-305'),('JPT Rotacion 5x2','1201-312'), "
    sql += "('FT Rotacion 5x2','1201-320'),('FT Rotacion 5x2','1201-323'),('JPT Rotacion 5x2','1201-330'), "
    sql += "('FT Rotacion 5x2','1201-337'),('JPT Rotacion 5x2','1201-340'),('Depto Display 2','1201-353'), "
    sql += "('FT Rotacion 5x2','1201-355'),('FT Rotacion 5x2','1400-302'),('FT Rotacion 5x2','1400-305'), "
    sql += "('FT Rotacion 5x2','1400-312'),('FT Rotacion 5x2','1400-315'),('FT Rotacion 5x2','1400-322'), "
    sql += "('FT Rotacion 5x2','1400-323'),('JPT Rotacion 5x2','1400-328'),('FT Rotacion 5x2','1400-328'), "
    sql += "('FT Rotacion 5x2','1400-334'),('FT Rotacion 5x2','1400-349'),('FT Rotacion 5x2','1400-352'), "
    sql += "('Depto Display 2','1400-353'),('JPM Rotacion 5x2','1445-309'),('FT Rotacion 5x2','1445-309'), "
    sql += "('JPT Rotacion 5x2','1445-309'),('JPT Rotacion 5x2','1445-323'),('Trastienda 1','1445-330'), "
    sql += "('Trastienda 1','1445-331'),('JPT Rotacion 5x2','1445-335'),('FT Rotacion 5x2','1445-337'), "
    sql += "('FT Rotacion 5x2','1445-338'),('FT Rotacion 5x2','1445-342'),('FT Rotacion 5x2','1445-352'), "
    sql += "('Seguridad 1','1445-352'),('Depto Display 1','1445-353'),('FT Rotacion 5x2','1485-305'), "
    sql += "('JPT Rotacion 5x2','1485-315'),('FT Rotacion 5x2','1485-322'),('FT Rotacion 5x2','1485-331'), "
    sql += "('FT Rotacion 5x2','1485-340'),('FT Rotacion 5x2','1485-346'),('FT Rotacion 5x2','1485-349'), "
    sql += "('Trastienda 2','1485-355'),('FT Rotacion 5x2','1501-302'),('JPT Rotacion 5x2','1501-305'), "
    sql += "('JPT Rotacion 5x2','1501-306'),('JPT Rotacion 5x2','1501-307'),('FT Rotacion 5x2','1501-307'), "
    sql += "('FT Rotacion 5x2','1501-309'),('FT Rotacion 5x2','1501-312'),('JPT Rotacion 5x2','1501-313'), "
    sql += "('FT Rotacion 5x2','1501-315'),('JPT Rotacion 5x2','1501-322'),('JPT Rotacion 5x2','1501-323'), "
    sql += "('FT Rotacion 5x2','1501-323'),('JPT Rotacion 5x2','1501-326'),('JPT Rotacion 5x2','1501-330'), "
    sql += "('FT Rotacion 5x2','1501-334'),('FT Rotacion 5x2','1501-337'),('Depto Abastecimiento 1 Jefes','1501-351'), "
    sql += "('FT Rotacion 5x2','1501-352'),('Seguridad 1','1501-352'),('Operador y Mantencion 1','1501-352'), "
    sql += "('Depto Display 1','1501-353'),('JPT Rotacion 5x2','1501-361'),('FT Ahumada','165-335'), "
    sql += "('JPM Rotacion 5x2','165-346'),('FT Rotacion 5x2','165-346'),('Trastienda Ahumada','165-355'), "
    sql += "('JPT Rotacion 5x2','165-364'),('FT Rotacion 5x2','1737-302'),('FT Rotacion 5x2','1737-305'), "
    sql += "('FT Rotacion 5x2','1737-307'),('FT Rotacion 5x2','1737-309'),('JPT Rotacion 5x2','1737-312'), "
    sql += "('FT Rotacion 5x2','1737-312'),('JPT Rotacion 5x2','1737-322'),('FT Rotacion 5x2','1737-322'), "
    sql += "('FT Rotacion 5x2','1737-328'),('FT Rotacion 5x2','1737-330'),('FT Rotacion 5x2','1737-335'), "
    sql += "('FT Rotacion 5x2','1737-352'),('JPT Rotacion 5x2','1737-361'),('FT Rotacion 5x2','1737-361'), "
    sql += "('FT Rotacion 5x2','1806-302'),('FT Rotacion 5x2','1806-313'),('FT Rotacion 5x2','1806-320'), "
    sql += "('FT Rotacion 5x2','1806-328'),('FT Rotacion 5x2','1806-334'),('FT Rotacion 5x2','1806-335'), "
    sql += "('FT Rotacion 5x2','1806-346'),('FT Rotacion 5x2','1806-352'),('JPT Rotacion 5x2','1806-361'), "
    sql += "('FT Rotacion 5x2','1806-361'),('FT Rotacion 5x2','2214-302'),('FT Rotacion 5x2','2214-305'), "
    sql += "('FT Rotacion 5x2','2214-312'),('FT Rotacion 5x2','2214-320'),('FT Rotacion 5x2','2214-330'), "
    sql += "('FT Rotacion 5x2','2214-346'),('FT Rotacion 5x2','2214-349'),('Seguridad 2','2214-352'), "
    sql += "('Depto Display 2','2214-353'),('JPT Rotacion 5x2','2381-309'),('JPT Rotacion 5x2','2381-312'), "
    sql += "('FT Rotacion 5x2','2381-328'),('FT Rotacion 5x2','2381-329'),('JPM Rotacion 5x2','2381-342'), "
    sql += "('FT Rotacion 5x2','2381-352'),('Probadores 1','2381-359'),('FT Rotacion 5x2','2381-361'), "
    sql += "('JPM Rotacion 5x2','242-302'),('JPM Rotacion 5x2','25-309'),('JPT Ahumada','25-309'), "
    sql += "('JPT Rotacion 5x2','25-312'),('FT Rotacion 5x2','25-315'),('FT Ahumada','25-315'), "
    sql += "('FT Ahumada','25-320'),('JPT Rotacion 5x2','25-361'),('FT Rotacion 5x2','2555-302'), "
    sql += "('FT Rotacion 5x2','2555-303'),('FT Rotacion 5x2','2555-305'),('JPT Rotacion 5x2','2555-312'), "
    sql += "('FT Rotacion 5x2','2555-322'),('FT Rotacion 5x2','2555-323'),('FT Rotacion 5x2','2555-326'), "
    sql += "('FT Rotacion 5x2','2555-346'),('FT Rotacion 5x2','2555-349'),('FT Rotacion 5x2','2555-352'), "
    sql += "('Depto Display 3','2555-353'),('FT Rotacion 5x2','2555-355'),('JPT Rotacion 5x2','2640-305'), "
    sql += "('FT Rotacion 5x2','2640-305'),('FT Rotacion 5x2','2640-307'),('FT Rotacion 5x2','2640-313'), "
    sql += "('FT Rotacion 5x2','2640-320'),('FT Rotacion 5x2','2640-323'),('FT Rotacion 5x2','2640-328'), "
    sql += "('FT Rotacion 5x2','2640-337'),('FT Rotacion 5x2','2640-346'),('FT Rotacion 5x2','2640-352'), "
    sql += "('Seguridad 2','2640-352'),('Depto Display 2','2640-353'),('FT Rotacion 5x2','2640-355'), "
    sql += "('FT Rotacion 5x2','2640-359'),('FT Rotacion 5x2','2640-361'),('FT Rotacion 5x2','2640-364'), "
    sql += "('JPT Rotacion 5x2','2775-305'),('FT Rotacion 5x2','2775-306'),('FT Rotacion 5x2','2775-312'), "
    sql += "('JPT Rotacion 5x2','2775-323'),('FT Rotacion 5x2','2775-323'),('FT Rotacion 5x2','2775-326'), "
    sql += "('FT Rotacion 5x2','2775-329'),('FT Rotacion 5x2','2775-332'),('JPT Rotacion 5x2','2775-349'), "
    sql += "('FT Rotacion 5x2','2775-349'),('FT Rotacion 5x2','2775-352'),('JPT Rotacion 5x2','2775-355'), "
    sql += "('FT Rotacion 5x2','2775-355'),('FT Rotacion 5x2','2775-361'),('FT Rotacion 5x2','2902-312'), "
    sql += "('FT Rotacion 5x2','2902-315'),('FT Rotacion 5x2','2902-322'),('FT Rotacion 5x2','2902-326'), "
    sql += "('FT Rotacion 5x2','2902-328'),('FT Rotacion 5x2','2902-346'),('FT Rotacion 5x2','2902-349'), "
    sql += "('FT Rotacion 5x2','2902-352'),('FT Rotacion 5x2','2902-359'),('JPT Rotacion 5x2','2990-305'), "
    sql += "('FT Rotacion 5x2','2990-307'),('JPM Rotacion 5x2','2990-322'),('Probadores 2','2990-322'), "
    sql += "('FT Rotacion 5x2','2990-322'),('FT Rotacion 5x2','2990-352'),('Analista Transacciones 2','2990-352'), "
    sql += "('FT Rotacion 5x2','2990-359'),('JPT Rotacion 5x2','3001-309'),('FT Rotacion 5x2','3001-320'), "
    sql += "('FT Rotacion 5x2','3001-352'),('Depto Display 1','3001-353'),('JPT Rotacion 5x2','3009-305'), "
    sql += "('FT Rotacion 5x2','3009-313'),('JPT Rotacion 5x2','3009-315'),('FT Rotacion 5x2','3009-320'), "
    sql += "('JPT Rotacion 5x2','3009-332'),('FT Rotacion 5x2','3009-332'),('FT Rotacion 5x2','3009-349'), "
    sql += "('Depto RRHH 1','3009-350'),('Depto Display 1','3009-353'),('FT Rotacion 5x2','3009-355'), "
    sql += "('Depto Tesoreria 1','3009-371'),('FT Rotacion 5x2','307-303'),('FT Rotacion 5x2','307-312'), "
    sql += "('JPT Rotacion 5x2','307-322'),('FT Rotacion 5x2','307-326'),('FT Rotacion 5x2','307-328'), "
    sql += "('FT Rotacion 5x2','307-331'),('FT Rotacion 5x2','307-346'),('Depto Display 3','307-353'), "
    sql += "('FT Rotacion 5x2','307-355'),('FT Rotacion 5x2','307-361'),('Probadores 1','312-307'), "
    sql += "('Depto RRHH 1','312-350'),('FT Rotacion 5x2','312-352'),('Operador y Mantencion 1','312-352'), "
    sql += "('Depto Display 1','312-353'),('FT Rotacion 5x2','312-355'),('JPT Rotacion 5x2','3177-302'), "
    sql += "('FT Rotacion 5x2','3177-302'),('JPT Rotacion 5x2','3177-305'),('FT Rotacion 5x2','3177-307'), "
    sql += "('JPT Rotacion 5x2','3177-309'),('FT Rotacion 5x2','3177-309'),('FT Rotacion 5x2','3177-312'), "
    sql += "('JPT Rotacion 5x2','3177-313'),('FT Rotacion 5x2','3177-313'),('FT Rotacion 5x2','3177-320'), "
    sql += "('FT Rotacion 5x2','3177-337'),('FT Rotacion 5x2','3177-352'),('Depto Display 2','3177-353'), "
    sql += "('FT Rotacion 5x2','3177-364'),('FT Rotacion 5x2','3296-305'),('FT Rotacion 5x2','3296-306'), "
    sql += "('JPT Rotacion 5x2','3296-312'),('JPT Rotacion 5x2','3296-313'),('FT Rotacion 5x2','3296-315'), "
    sql += "('JPT Rotacion 5x2','3296-322'),('FT Rotacion 5x2','3296-322'),('FT Rotacion 5x2','3296-330'), "
    sql += "('JPT Rotacion 5x2','3296-331'),('JPT Rotacion 5x2','3296-346'),('FT Rotacion 5x2','3296-361'), "
    sql += "('FT Rotacion 5x2','3296-364'),('FT Ahumada','366-323'),('Probadores 2','438-307'), "
    sql += "('FT Rotacion 5x2','438-309'),('FT Rotacion 5x2','438-346'),('FT Rotacion 5x2','438-352'), "
    sql += "('Operador y Mantencion 2','438-352'),('Depto Display 2','438-353'),('FT Rotacion 5x2','438-355'), "
    sql += "('JPT Rotacion 5x2','438-361'),('FT Rotacion 5x2','438-364'),('FT Rotacion 5x2','439-332'), "
    sql += "('FT Rotacion 5x2','472-302'),('JPT Rotacion 5x2','472-309'),('JPM Rotacion 5x2','472-312'), "
    sql += "('FT Rotacion 5x2','472-328'),('FT Rotacion 5x2','472-330'),('FT Rotacion 5x2','472-352'), "
    sql += "('Depto Display 2','472-353'),('FT Rotacion 5x2','472-361'),('FT Rotacion 5x2','510-302'), "
    sql += "('JPT Rotacion 5x2','510-309'),('JPM Rotacion 5x2','510-312'),('FT Rotacion 5x2','510-312'), "
    sql += "('JPM Rotacion 5x2','510-320'),('FT Rotacion 5x2','510-326'),('FT Rotacion 5x2','510-352'), "
    sql += "('Depto Display 3','510-353'),('FT Rotacion 5x2','510-361'),('FT Rotacion 5x2','530-302'), "
    sql += "('FT Rotacion 5x2','530-303'),('FT Rotacion 5x2','530-305'),('FT Rotacion 5x2','530-322'), "
    sql += "('JPM Rotacion 5x2','530-326'),('FT Rotacion 5x2','530-326'),('FT Rotacion 5x2','530-328'), "
    sql += "('FT Rotacion 5x2','530-330'),('FT Rotacion 5x2','530-334'),('FT Rotacion 5x2','530-337'), "
    sql += "('FT Rotacion 5x2','530-346'),('Depto RRHH 1','530-350'),('FT Rotacion 5x2','530-352'), "
    sql += "('Operador y Mantencion 1','530-352'),('Depto Display 1','530-353'),('FT Rotacion 5x2','530-355'), "
    sql += "('FT Rotacion 5x2','530-359'),('JPM Rotacion 5x2','530-361'),('FT Rotacion 5x2','530-361'), "
    sql += "('FT Rotacion 5x2','530-364'),('Depto Tesoreria 1','530-371'),('FT Rotacion 5x2','530-373'), "
    sql += "('FT Rotacion 5x2','5413-302'),('JPT Rotacion 5x2','5413-305'),('JPT Rotacion 5x2','5413-307'), "
    sql += "('FT Rotacion 5x2','5413-307'),('JPM Rotacion 5x2','5413-309'),('FT Rotacion 5x2','5413-309'), "
    sql += "('JPT Rotacion 5x2','5413-309'),('Probadores 1','5413-309'),('JPT Rotacion 5x2','5413-312'), "
    sql += "('FT Rotacion 5x2','5413-312'),('JPM Rotacion 5x2','5413-315'),('FT Rotacion 5x2','5413-323'), "
    sql += "('FT Rotacion 5x2','5413-328'),('FT Rotacion 5x2','5413-331'),('JPT Rotacion 5x2','5413-335'), "
    sql += "('JPM Rotacion 5x2','5413-337'),('FT Rotacion 5x2','5413-342'),('FT Rotacion 5x2','5413-346'), "
    sql += "('FT Rotacion 5x2','5413-349'),('Depto Display 1','5413-353'),('FT Rotacion 5x2','5413-355'), "
    sql += "('Trastienda 1','5413-355'),('JPT Rotacion 5x2','5413-361'),('FT Rotacion 5x2','5413-361'), "
    sql += "('Probadores 1','5413-361'),('JPM Rotacion 5x2','570-303'),('JPT Rotacion 5x2','570-303'), "
    sql += "('FT Rotacion 5x2','570-305'),('Probadores JP30','570-309'),('JPT Rotacion 5x2','570-312'), "
    sql += "('FT Rotacion 5x2','570-322'),('JPM Rotacion 5x2','570-323'),('JPT Rotacion 5x2','570-335'), "
    sql += "('JPT Rotacion 5x2','570-340'),('JPM Rotacion 5x2','570-342'),('JPT Rotacion 5x2','570-342'), "
    sql += "('JPT Rotacion 5x2','570-343'),('JPM Rotacion 5x2','570-346'),('FT Rotacion 5x2','570-352'), "
    sql += "('Depto Display 2','570-353'),('JPT Rotacion 5x2','570-361'),('JPM Rotacion 5x2','570-364'), "
    sql += "('JPT Rotacion 5x2','570-364'),('Depto Tesoreria 2','570-371'),('JPT Rotacion 5x2','603-302'), "
    sql += "('FT Rotacion 5x2','603-302'),('JPT Rotacion 5x2','603-305'),('JPT Rotacion 5x2','603-307'), "
    sql += "('JPM Rotacion 5x2','603-309'),('FT Rotacion 5x2','603-312'),('JPT Rotacion 5x2','603-322'), "
    sql += "('JPT Rotacion 5x2','603-328'),('FT Rotacion 5x2','603-329'),('FT Rotacion 5x2','603-340'), "
    sql += "('JPM Rotacion 5x2','603-346'),('Depto Display 3','603-353'),('JPT Rotacion 5x2','603-355'), "
    sql += "('FT Rotacion 5x2','603-355'),('JPT Rotacion 5x2','603-361'),('FT Rotacion 5x2','603-361'), "
    sql += "('FT Rotacion 5x2','603-364'),('Depto Tesoreria 3','603-371'),('JPT Rotacion 5x2','70-305'), "
    sql += "('FT Rotacion 5x2','70-305'),('JPT Rotacion 5x2','70-306'),('Trastienda 1','70-306'), "
    sql += "('FT Rotacion 5x2','70-307'),('FT Rotacion 5x2','70-309'),('Probadores 1','70-309'), "
    sql += "('FT Rotacion 5x2','70-315'),('FT Rotacion 5x2','70-320'),('FT Rotacion 5x2','70-322'), "
    sql += "('Probadores 1','70-323'),('JPT Rotacion 5x2','70-330'),('FT Rotacion 5x2','70-330'), "
    sql += "('Trastienda 1','70-331'),('FT Rotacion 5x2','70-346'),('FT Rotacion 5x2','70-349'), "
    sql += "('Depto RRHH 1','70-350'),('Depto Abastecimiento 1 Jefes','70-351'),('FT Rotacion 5x2','70-352'), "
    sql += "('Depto Display 1','70-353'),('FT Rotacion 5x2','70-361'),('FT Rotacion 5x2','70-364'), "
    sql += "('JPT Rotacion 5x2','7200-302'),('JPT Rotacion 5x2','7200-305'),('JPT Rotacion 5x2','7200-307'), "
    sql += "('JPM Rotacion 5x2','7200-309'),('JPM Rotacion 5x2','7200-312'),('JPT Rotacion 5x2','7200-312'), "
    sql += "('FT Rotacion 5x2','7200-312'),('FT Rotacion 5x2','7200-315'),('JPM Rotacion 5x2','7200-322'), "
    sql += "('FT Rotacion 5x2','7200-322'),('JPM Rotacion 5x2','7200-323'),('JPT Rotacion 5x2','7200-323'), "
    sql += "('FT Rotacion 5x2','7200-326'),('JPT Rotacion 5x2','7200-328'),('JPT Rotacion 5x2','7200-330'), "
    sql += "('FT Rotacion 5x2','7200-335'),('JPT Rotacion 5x2','7200-349'),('Seguridad 1','7200-352'), "
    sql += "('Depto Display 1','7200-353'),('JPT Rotacion 5x2','7200-355'),('FT Rotacion 5x2','7200-359'), "
    sql += "('FT Rotacion 5x2','7200-361'),('Depto Tesoreria 1','7200-371'),('FT Rotacion 5x2','739-303'), "
    sql += "('FT Rotacion 5x2','739-305'),('FT Rotacion 5x2','739-312'),('FT Rotacion 5x2','739-323'), "
    sql += "('FT Rotacion 5x2','739-326'),('FT Rotacion 5x2','739-335'),('FT Rotacion 5x2','739-337'), "
    sql += "('FT Rotacion 5x2','739-352'),('Depto Display 3','739-353'),('FT Rotacion 5x2','739-359'), "
    sql += "('FT Rotacion 5x2','739-361'),('Depto RRHH 3','802-350'),('Depto Abastecimiento Concepcion','802-351'), "
    sql += "('FT Rotacion 5x2','802-352'),('Depto Display 3','802-353'),('FT Rotacion 5x2','810-307'), "
    sql += "('FT Rotacion 5x2','810-312'),('FT Rotacion 5x2','810-328'),('FT Rotacion 5x2','810-330'), "
    sql += "('FT Rotacion 5x2','810-331'),('FT Rotacion 5x2','810-364'),('JPM Rotacion 5x2','836-305'), "
    sql += "('JPM Rotacion 5x2','836-307'),('FT Rotacion 5x2','836-307'),('JPM Rotacion 5x2','836-312'), "
    sql += "('FT Rotacion 5x2','836-312'),('JPT Rotacion 5x2','836-312'),('JPT Rotacion 5x2','836-313'), "
    sql += "('JPT Rotacion 5x2','836-320'),('JPT Rotacion 5x2','836-322'),('JPT Rotacion 5x2','836-326'), "
    sql += "('JPT Rotacion 5x2','836-328'),('FT Rotacion 5x2','836-330'),('JPT Rotacion 5x2','836-331'), "
    sql += "('JPM Rotacion 5x2','836-342'),('JPT Rotacion 5x2','836-346'),('FT Rotacion 5x2','836-349'), "
    sql += "('JPT Rotacion 5x2','836-355'),('JPT Rotacion 5x2','836-359'),('FT Rotacion 5x2','836-359'), "
    sql += "('JPT Rotacion 5x2','836-361'),('JPT Rotacion 5x2','878-302'),('JPM Rotacion 5x2','878-309'), "
    sql += "('Probadores JP30','878-309'),('JPT Rotacion 5x2','878-309'),('JPM Rotacion 5x2','878-312'), "
    sql += "('JPT Rotacion 5x2','878-312'),('FT Rotacion 5x2','878-331'),('JPT Rotacion 5x2','878-364'), "
    sql += "('JPT Rotacion 5x2','9001-305'),('FT Rotacion 5x2','9001-305'),('FT Rotacion 5x2','9001-309'), "
    sql += "('FT Rotacion 5x2','9001-315'),('JPT Rotacion 5x2','9001-322'),('JPT Rotacion 5x2','9001-323'), "
    sql += "('FT Rotacion 5x2','9001-327'),('FT Rotacion 5x2','9001-338'),('FT Rotacion 5x2','9001-340'), "
    sql += "('FT Rotacion 5x2','9001-342'),('FT Rotacion 5x2','9001-346'),('FT Rotacion 5x2','9001-349'), "
    sql += "('Depto Display 1','9001-353'),('FT Rotacion 5x2','9001-355'),('FT Rotacion 5x2','9001-361'))) rot "
    sql += "group by rot.sched_rotation_id, rot.org_entry_id, rot.semana, rot.number_of_weeks "

    #rot.sched_rotation_id, 
    #rot.org_entry_id, 
    #rot.semana, 
    #rot.number_of_weeks, 
    #count(*)
    cursor = conn.cursor()
    cursor.execute(sql)
    rot_bal = cursor.fetchall()
    cursor.close()
    
    d_rot_bal = dict()
    
    for next_rot in rot_bal:
        key = next_rot[0].__str__()+ next_rot[1].__str__()
        if key not in d_rot_bal:
            d_rot_bal[key] = rotation_balance(next_rot[0],next_rot[3],next_rot[1])
        d_rot_bal[key].set_week_balance(next_rot[2], next_rot[4])
        
    return d_rot_bal

def get_emps_for_week(conn, id, org_id, week):
    sql = "select esr.emp_id, esr.week_counter, esr.eff_sdate "
    sql += "from emp_sched_rotation esr, sched_rotation sr, emp_org_position eop, org_position op "
    sql += "where esr.sched_rotation_id = "+id.__str__()+" "
    sql += "and esr.emp_id = eop.emp_id "
    sql += "and eop.org_position_id = op.org_position_id "
    sql += "and sr.sched_rotation_id = esr.sched_rotation_id "
    sql += "and eop.eff_date < to_date('20100906','yyyymmdd') "
    sql += "and (eop.end_date is null or eop.end_date > to_date('20100830','yyyymmdd')) "
    sql += "and esr.eff_sdate < '20100906' "
    sql += "and (esr.end_sdate is null or esr.end_sdate >= '20100830') "
    sql += "and op.org_entry_id = "+org_id.__str__()+" "
    sql += "and "+week.__str__()+" =mod((trunc(to_date('30-08-2010', 'dd-mm-yyyy'), 'd') - "
    sql += "           trunc(to_date(esr.eff_sdate, 'yyyymmdd'), 'd')) / 7 + "
    sql += "           esr.week_counter, "
    sql += "           sr.number_of_weeks) + 1 "

    cursor = conn.cursor()
    cursor.execute(sql)
    emps = cursor.fetchall()
    cursor.close()

    return emps
def get_better(conn):
    
    movable_emps = get_emps_to_move(conn)
    rot = get_rotation_bal(conn)
    
    for key in rot.keys():
        week = rot[key].evaluate_balance()
        if week != -1:
            max_rot_emps = get_emps_for_week(conn, rot[key].id, rot[key].org_id, week)
            for next_emp in max_rot_emps:
                if next_emp[0] in movable_emps:
                    delta = rot[key].rebalance(week)
                    rot_stat = rot[key].evaluate_balance()
                    
                    next_week = next_emp[1] + delta
                    if next_week > rot[key].weeks:
                        next_week -= rot[key].weeks
                    elif next_week < 1:
                        next_week += rot[key].weeks
                    sql = "update emp_sched_rotation set week_counter = " +next_week.__str__()
                    sql += " where sched_rotation_id = " + rot[key].id.__str__()
                    sql += " and emp_id = " + next_emp[0].__str__()
                    sql += " and eff_sdate = '" + next_emp[2] + "';"
                    print(sql)
                    if rot_stat == -1:
                        print("Rot : " + rot[key].id.__str__() + " in org : " + rot[key].org_id.__str__() + " could be fixed")
                        break
                    else:
                        print("Rot : " + rot[key].id.__str__() + " in org : " + rot[key].org_id.__str__() + " little better")
         
        
def get_constraint_str(detail):
    dom = parseString(detail)
    d_avail = {'2':"0",'3':"0",'4':"0",'5':"0",'6':"0",'7':"0",'1':"0"}
    
    dbes = dom.getElementsByTagName("dbe")
    for day in dbes:
        d_el=day.getElementsByTagName("d")
        jpar = False
        if len(d_el)> 0:
            b_el = day.getElementsByTagName("b")
            if len(b_el) > 0:
                b_hour = b_el[0].firstChild.nodeValue
                e_el = day.getElementsByTagName("e")
                if len(e_el) > 0:
                    e_hour = b_el[0].firstChild.nodeValue
                    if (b_hour == '2345' and e_hour == '00'):
                        jpar = True
            if not jpar:
                d_avail[d_el[0].firstChild.nodeValue] = "1"
    return d_avail['2']+d_avail['3']+d_avail['4']+d_avail['5']+d_avail['6']+d_avail['7']+d_avail['1']
    
def get_rot_detail(conn, rot):
    sql = "select srd.sched_rotation_week, srd.day_id " 
    sql += "from sched_rotation_detail srd "
    sql += "where srd.sched_rotation_id = " + rot.id.__str__()
    sql += "order by srd.sched_rotation_week, srd.day_id"

    cursor = conn.cursor()
    cursor.execute(sql)
    rot_det = cursor.fetchall()
    cursor.close()
    if len(rot_det)> 0:
        curr_week= 0
        s_avail = dict()
        for next_det in rot_det:
            if next_det[0] != curr_week:
                if curr_week != 0:
                    rot.avail[curr_week] = s_avail[2]+s_avail[3]+s_avail[4]+s_avail[5]+s_avail[6]+s_avail[7]+s_avail[1]
                curr_week = next_det[0]
                s_avail = {2:"0",3:"0",4:"0",5:"0",6:"0",7:"0",1:"0"}
            s_avail[next_det[1]] = "1"
        if curr_week != 0:
            rot.avail[curr_week] = s_avail[2]+s_avail[3]+s_avail[4]+s_avail[5]+s_avail[6]+s_avail[7]+s_avail[1]
                
def get_rotations(conn):
    sql = "select sr.sched_rotation_id, sr.number_of_weeks "
    sql += "from sched_rotation sr "
    sql += "where sr.sched_rotation_id in ("
    sql += "select esr.sched_rotation_id "
    sql += "from emp_sched_rotation esr, v_emp e, emp_status es "
    sql += "where esr.emp_id = e.emp_id "
    sql += "and es.emp_id = e.emp_id "
    sql += "and esr.eff_sdate < to_char(sysdate, 'yyyymmdd') "
    sql += "and (esr.end_sdate is null or esr.end_sdate >= to_char(sysdate, 'yyyymmdd')) "
    sql += "and es.emp_status_id = 1 "
    sql += "and es.eff_date < sysdate "
    sql += "and (es.end_date is null or es.end_date >= sysdate))"
    
    cursor = conn.cursor()
    cursor.execute(sql)
    rots = cursor.fetchall()
    cursor.close()
    
    d_rot = dict()
    if (len(rots) > 0):
        for next_rot in rots:
            d_rot[next_rot[0]] = rotation(next_rot[0], next_rot[1])
            get_rot_detail(conn, d_rot[next_rot[0]])
    return d_rot
    
def get_last_monday(conn, start_date):
    sql = "select to_char(to_date('"+start_date+"','yyyymmdd')-1 "
    sql += "- to_number(to_char(to_date('" + start_date + "','yyyymmdd')-1,'d'))+1,'yyyymmdd') from dual"
    cursor = conn.cursor()
    cursor.execute(sql)
    monday = cursor.fetchone()
    cursor.close()
    return monday[0]

def get_next_monday(conn, last_monday ):
    sql = "select to_char(to_date('" + last_monday + "', 'yyyymmdd') + 7,'yyyymmdd') from dual"
    cursor = conn.cursor()
    cursor.execute(sql)
    monday = cursor.fetchone()
    cursor.close()
    return monday[0]

def get_emp_avail(conn, emp_id,last_monday, next_monday, org_id):
    
    s_avail= ""
    sql = "select count(*) "
    sql += "from sched_build_emp sbe "
    sql += "where sbe.emp_id = " + emp_id.__str__() + " "
    sql += "and sbe.build_id in (select unique build_id "
    sql += "from sched_build_org sbo "
    sql += "where sbo.start_sdate < '20100830' "
    sql += "and sbo.start_sdate >= '20100802' "
    sql += "and sbo.org_entry_id = "+org_id.__str__()+")"

    cursor = conn.cursor()
    cursor.execute(sql)
    build_count = cursor.fetchone()
    cursor.close()

    if build_count[0] > 0:
        
        
        sql = "select t.emp_id " 
        sql += "from rqst t "
        sql += "where t.rqst_type_id = 1 "
        sql += "and t.rqst_status_cd_id = 2 "
        sql += "and t.emp_id = " + emp_id.__str__()
        sql += "and t.reqst_eff_sdate < '" + next_monday + "' "
        sql += "and t.reqst_exp_sdate >= '" + last_monday + "'"
    
        cursor = conn.cursor()
        cursor.execute(sql)
        emp_rqst = cursor.fetchone()
        cursor.close()
        
        if emp_rqst is not None:
            #print("emp id: " + emp_id.__str__()+ ",")
            sql = "select sc.sched_constraint_value_detail "
            sql += "from sched_constraint sc "
            sql += "where eff_sdate = '"+last_monday+"' "
            sql += "and end_sdate = to_char(to_date('"+next_monday+"','yyyymmdd')-1,'yyyymmdd') "
            sql += "and emp_id = "+emp_id.__str__()+" "
            sql += "and org_entry_id = "+org_id.__str__()+" "
            sql += "and sched_constraint_type_id = 1"
            cursor = conn.cursor()
            cursor.execute(sql)
            emp_const = cursor.fetchone()
            cursor.close()
            if emp_const is not None:
                s_avail = get_constraint_str(emp_const[0])
            else:
                s_avail = "**"
        else:
            sql = "select to_number(to_char(s.start_date,'d')) dia "
            sql += "from shift s "
            sql += "where s.emp_id = " + emp_id.__str__()
            sql += " and s.start_date between to_date('" + last_monday + " 00:00:00','yyyymmdd hh24:mi:ss') "
            sql += "and to_date('" + next_monday + " 00:00:00','yyyymmdd hh24:mi:ss') "
            sql += "and s.shift_state_type_id = 1 "
            sql += "order by dia"
            
            cursor = conn.cursor()
            cursor.execute(sql)
            emp_avail = cursor.fetchall()
            cursor.close()
            
            if (len(emp_avail) > 0):
                l_avail = ["0","0","0","0","0","0","0"]
                for next_emp in emp_avail:
                    #print(next_emp)
                    l_avail[int(next_emp[0])-1] = "1"
                s_avail = l_avail[0]+l_avail[1]+l_avail[2]+l_avail[3]+l_avail[4]+l_avail[5]+l_avail[6]
    return s_avail 
    
    
def get_emps_to_verify(conn, start_date, end_date, comp_sdate, comp_edate):
    #Columns to get:
    # 0: employee id
    # 1: rotation id
    # 2: rotation week applied to this week
    # 3: week counter
    # 4: emp-rot effective date
    # 5: HR employee id
    # 6: last name
    # 7: first name
    # 8: org id
    # 9: org_code
    #10: position id
    #11: pos eff date
    #12: pos end date
    #13: schedule plan id
    #14: sched plan eff date
    #15: sched plan end date
    #16: emp rot end date
    sql = "select esr.emp_id, sr.sched_rotation_id, " 
    sql += "mod((trunc(to_date('" + comp_sdate + "','yyyymmdd') - (to_date(esr.eff_sdate,'yyyymmdd')- to_number(to_char(to_date(esr.eff_sdate, 'yyyymmdd'),'d'))+1))/7),sr.number_of_weeks)+esr.week_counter, "
    sql += "esr.week_counter, esr.eff_sdate, e.hr_emp_id, e.last_name, e.first_name, " 
    sql += "oe.org_entry_id, oe.org_entry_cd, op.org_position_id, to_char(eop.eff_date,'yyyymmdd'), "
    sql += "to_char(nvl(eop.end_date,to_date('20101231','yyyymmdd')),'yyyymmdd'), esp.sched_plan_id, esp.eff_sdate, "
    sql += "esp.end_sdate, esr.end_sdate "
    sql += "from emp_sched_rotation esr, sched_rotation sr, org_sched_rotation osr, emp_org_position eop, " 
    sql += "org_position op, v_emp e, org_entry oe, emp_status es, org_status os, emp_sched_plan esp "
    sql += "where e.emp_id= esr.emp_id  "
    sql += "and sr.sched_rotation_id = esr.sched_rotation_id " 
    sql += "and osr.sched_rotation_id = sr.sched_rotation_id  "
    sql += "and oe.org_entry_id = op.org_entry_id  "
    sql += "and eop.emp_id = esr.emp_id  "
    sql += "and eop.org_position_id = op.org_position_id " 
    sql += "and op.org_entry_id = osr.org_entry_id  "
    sql += "and os.org_entry_id = oe.org_entry_id  "
    sql += "and es.emp_id = e.emp_id  "
    sql += "and esp.emp_id = e.EMP_ID "
    sql += "and es.emp_status_id = 1  "
    sql += "and os.status_id = 1  "
    sql += "and esp.eff_sdate < '"+end_date+"' "
    sql += "and (esp.end_sdate is null or esp.end_sdate >= '"+start_date+"') "
    sql += "and es.eff_date < to_date('"+end_date+"','yyyymmdd')  "
    sql += "and (es.end_date is null or es.end_date >= to_date('"+start_date+"','yyyymmdd')) " 
    sql += "and os.eff_date < sysdate  "
    sql += "and (os.end_date is null or os.end_date >= sysdate) " 
    sql += "and eop.eff_date < to_date('"+end_date+"','yyyymmdd') " 
    sql += "and (eop.end_date is null or eop.end_date >= to_date('"+start_date+"','yyyymmdd')) " 
    sql += "and osr.eff_sdate < '"+end_date+"'  "
    sql += "and (osr.end_sdate is null or osr.end_sdate >= '"+start_date+"') " 
    sql += "and esr.eff_sdate < '"+start_date+"'  "
    sql += "and (esr.end_sdate is null or esr.end_sdate > '"+start_date+"') " 
    #sql += "and oe.org_entry_cd like '70-%' "
    sql += "order by esr.emp_id, oe.org_entry_id, sr.sched_rotation_id"
    #sql += "and (oe.org_entry_cd like '1400-%' or oe.org_entry_cd like '1201-%' or oe.org_entry_cd like '1501-%' or oe.org_entry_cd like '438-%' or oe.org_entry_cd like '472-%' or oe.org_entry_cd like '570-%') "
    
    #print(sql)
    
    cursor = conn.cursor()
    cursor.execute(sql)
    emp_rot = cursor.fetchall()
    cursor.close()
    return emp_rot
            
def get_emps_to_fix(conn, start_date, end_date):
    last_monday = get_last_monday(conn, start_date)
    next_monday = get_next_monday(conn, last_monday)

    #Paso 1, obtener rotatciones
    d_rots = get_rotations(conn)
    #Paso 2, obtener empleados con rotación
    t_emps = get_emps_to_verify(conn, start_date, end_date, last_monday, next_monday)
    
    d_emps_to_fix = dict()
    if len(t_emps)> 0:
        for next_emp in t_emps:
            # 0: employee id
            # 1: rotation id
            # 2: rotation week applied to this week
            # 3: week counter
            # 4: emp-rot effective date
            # 5: HR employee id
            # 6: last name
            # 7: first name
            # 8: org id
            # 9: org_code
            #10: position id
            #11: pos eff date
            #12: pos end date
            #13: schedule plan id
            #14: sched plan eff date
            #15: sched plan end date
            #16: emp rot end date
            #Paso 2.1 obtener disponibilidad del empleado
            if (next_emp[15] is not None) and int(start_date) < int(next_emp[15]):
                emp_avail = ""
            elif int(start_date) < int(next_emp[11]):
                emp_avail = ""
            else: 
                emp_avail = get_emp_avail(conn,next_emp[0], last_monday, next_monday,next_emp[8] )
            if emp_avail == "**":
                print(next_emp[9] + " - Emp: " + next_emp[5] + "-" + next_emp[6] + "-" + next_emp[7])
                emp_avail = ""
            if len(emp_avail)>0:
                rot = d_rots[next_emp[1]]
                rot_week = 0
                emp_week = next_emp[2]
                if emp_week > rot.weeks:
                    emp_week = emp_week - rot.weeks  
                #Paso 2.2 identificar semana de la rotación coincidente con disponibilidad 
                for week in range(rot.weeks):
                    if rot.avail[week + 1] == emp_avail:
                        rot_week = week + 1
                        break
                if rot_week != emp_week and rot_week != 0:
                    new_week = 0
                    if rot_week > emp_week:
                        new_week = next_emp[3] + (rot_week - emp_week)
                        if new_week > rot.weeks:
                            new_week -= rot.weeks
                    else:
                        new_week = next_emp[3] - (emp_week-rot_week)
                        if new_week < 1:
                            new_week += rot.weeks
                    d_emps_to_fix[next_emp[0]] = [next_emp[0],next_emp[1], next_emp[3], new_week, next_emp[5],next_emp[6], next_emp[7]]
                    #print("Emp: " + next_emp[5] + "-" + next_emp[6] + "-" + next_emp[7] + " actual week " + next_emp[3].__str__() + " and should be "+ new_week.__str__())
                    print("update emp_sched_rotation set week_counter = " + new_week.__str__() + " where emp_id = " + next_emp[0].__str__() + " and sched_rotation_id = " + next_emp[1].__str__() + " and eff_sdate = '"+next_emp[4]+"';")
            #else:
            #    print(next_emp[9] + " - Emp: " + next_emp[5] + "-" + next_emp[6] + "-" + next_emp[7])

    return d_emps_to_fix
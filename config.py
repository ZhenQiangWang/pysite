INSERT_SQL = '''
merge into GRAPSETINFO t1
            using (select 
            :v0 as PRODUCT,
            :v1 as ITEMS,
            :v2 as QTY,
            :v3 as UPPER,
            :v4 as LOWER
            from dual
            ) t2
            on(
            t1.PRODUCT = t2.PRODUCT
            and t1.ITEMS = t2.ITEMS
            )
            when matched then update set   
              t1.QTY = t2.QTY,
              t1.UPPER = t2.UPPER,
              t1.LOWER = t2.LOWER
            when not matched then
              insert values(
              t2.PRODUCT,
              t2.ITEMS,
              t2.QTY,
              t2.UPPER,
              t2.LOWER
              )
'''


DEL_SQL = '''
delete from GRAPSETINFO where PRODUCT = :v0 and ITEMS = :v1
'''


QUERY_DATA_SQL = '''
    SELECT VALUE_NUM FROM (
        select* from FT_CERAMIC_DIERAW where 1=1
          and PF = 'Pass'
          and LATEST_FLAG = 'Y'
          and CUSTOMER_PRODUCT = :v0
          and PARAMETER = :v1
          and LOT = :v2
          and VALUE_NUM > :v3
          and VALUE_NUM < :v4
          ORDER BY DBMS_RANDOM.RANDOM()
    ) WHERE ROWNUM <= :v5
'''

QUERY_CONFIG_SQL = '''
select * from GRAPSETINFO where 1=1
'''

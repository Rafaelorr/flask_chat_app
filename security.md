# security:
    - sql injection:
        - gebruik nooit excutescripts
        - gebruik dit voor insert stamtents cursor.execute("INSERT INTO test_table VALUES(?, ?, ?)", data)
Attribute VB_Name = "Mod_SQL"
Option Explicit

' Simple ODBC pull: requires a DSN configured in Windows ODBC named "MES_DSN"
' and a table "readings" with columns (ts DATETIME, machine TEXT, s1 DOUBLE)
Public Sub ImportFromODBC()
    Dim cn As Object, rs As Object
    Set cn = CreateObject("ADODB.Connection")
    Set rs = CreateObject("ADODB.Recordset")
    On Error GoTo EH

    cn.Open "DSN=MES_DSN;"
    rs.Open "SELECT TOP 100 ts, machine, s1 FROM readings ORDER BY ts DESC;", cn

    Dim ws As Worksheet: Set ws = ThisWorkbook.Sheets("Sheet1")
    ws.Cells.Clear
    ws.Range("A1:C1").Value = Array("ts", "machine", "s1")
    Dim r As Long: r = 2
    Do While Not rs.EOF
        ws.Cells(r, 1).Value = rs.Fields(0).Value
        ws.Cells(r, 2).Value = rs.Fields(1).Value
        ws.Cells(r, 3).Value = rs.Fields(2).Value
        r = r + 1
        rs.MoveNext
    Loop
    rs.Close: cn.Close
    MsgBox "ODBC import completed: " & (r - 2) & " rows"
    Exit Sub
EH:
    MsgBox "ODBC error: " & Err.Description
End Sub

Attribute VB_Name = "Mod_SPC"
Option Explicit

' Generates an Xbar-R chart from data in Sheet1 columns A..E (A: subgroup id, B..E: measurements)
' Output goes to Sheet2.
Public Sub MakeXbarR()
    Dim ws As Worksheet, outWs As Worksheet
    Set ws = ThisWorkbook.Sheets("Sheet1")
    Set outWs = ThisWorkbook.Sheets("Sheet2")
    outWs.Cells.Clear

    Dim lastRow As Long: lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    Dim n As Long: n = lastRow - 1
    Dim g As Long, i As Long, j As Long
    Dim k As Long: k = 4 ' subgroup size (B..E)

    outWs.Range("A1:E1").Value = Array("Subgroup", "Xbar", "R", "UCL", "LCL")

    Dim mu As Double, sigma As Double
    mu = WorksheetFunction.Average(ws.Range("B2:E" & lastRow))
    sigma = WorksheetFunction.StDev_P(ws.Range("B2:E" & lastRow))

    For i = 2 To lastRow
        Dim xbar As Double, xmax As Double, xmin As Double
        xbar = WorksheetFunction.Average(ws.Range("B" & i & ":E" & i))
        xmax = WorksheetFunction.Max(ws.Range("B" & i & ":E" & i))
        xmin = WorksheetFunction.Min(ws.Range("B" & i & ":E" & i))
        outWs.Cells(i - 1, 1).Value = ws.Cells(i, 1).Value
        outWs.Cells(i - 1, 2).Value = xbar
        outWs.Cells(i - 1, 3).Value = xmax - xmin
        outWs.Cells(i - 1, 4).Value = mu + 3 * sigma
        outWs.Cells(i - 1, 5).Value = mu - 3 * sigma
    Next i

    ' Basic chart
    Dim cht As ChartObject
    Set cht = outWs.ChartObjects.Add(Left:=300, Top:=20, Width:=600, Height:=300)
    cht.Chart.ChartType = xlLine
    cht.Chart.SetSourceData Source:=outWs.Range("A1:E" & n)
    cht.Chart.HasTitle = True
    cht.Chart.ChartTitle.Text = "Xbar-R Chart"
End Sub

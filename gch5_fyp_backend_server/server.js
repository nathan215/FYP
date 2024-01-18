const express = require('express');
const XLSX = require('xlsx');
const app = express();
const port = 3000;
const cors = require('cors');


app.use(cors());

app.get('/', (req, res) => {
    res.send('Node.js server is running');
  });

  
app.get('/get-excel-data', (req, res) => {
  // Path ..\data.xlsx
  const filePath = 'data.xlsx';

  // Read the Excel file
  const workbook = XLSX.readFile(filePath);
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];
  const data = XLSX.utils.sheet_to_json(worksheet);

  // Send the data back as JSON
  res.json(data);
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

const express = require('express');
const router = express.Router();
const XLSX = require('xlsx');

router.get('/', (req, res) => {
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

module.exports = router;
// SET STORAGE
const multer = require('multer');
const fs = require("fs");
const path = require('path');

const storage_image = multer.diskStorage({
  filename: (req, file, cb) => {
      cb(null, file.originalname);
  },
  destination: (req, file, cb) => {
      // const str = path.join(__dirname, '../public/img/')
      cb(null, path.join(__dirname, "../public/img"));
  },
});

const storage_model = multer.diskStorage({
  destination: (req, file, cb) => {
      cb(null, path.join(__dirname, '../public/model'));
  },
  filename: (req, file, cb) => {
      cb(null, file.originalname);
  }
});

exports.upload_image = multer({ storage: storage_image })
exports.upload_model = multer({ storage: storage_model })

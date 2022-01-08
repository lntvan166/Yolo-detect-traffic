const express = require('express');
const router = express.Router();
const {
    upload_model
} = require('../services/multer')
const fs = require("fs");
const path = require('path');

router.get('/upload-model', (req, res) => {
    const hasModel = fs.existsSync(path.join(__dirname, '../../best.pt'));
    return res.render('upload-model', {
        hasModel
    });
});

router.post('/upload-model', upload_model.single('data-model'), (req, res) => {
    const extAccept = ['.pt', '.pth']
    const extname = path.extname(req.file.originalname).toLowerCase()

    if (extAccept.includes(extname)) {
				fs.unlinkSync(path.join(__dirname, "../public/model/best.pt"));
        fs.rename(
            path.join(__dirname, '../public/model/', req.file.originalname),
            path.join(__dirname, '../public/model/', 'best.pt'),
            (err) => {
                if (err) throw err;
            }
        );
        fs.unlinkSync(path.join(__dirname, "../../best.pt"));
        const path_src = path.join(__dirname, "../public/model/best.pt");
        const path_dst = path.join(__dirname, "../../best.pt");
        fs.copyFile(path_src, path_dst, (err) => {
            if (err) {
                console.log(err);
            }
            console.log("Copy file done.");
        });
        const hasModel = true
        return res.render('upload-model', {
            hasModel
        });
    }
    fs.unlinkSync(path.join(__dirname, '../../', req.file.originalname));
    const notSupport = true
    return res.render('upload-model', {
        notSupport
    });
});


module.exports = router;

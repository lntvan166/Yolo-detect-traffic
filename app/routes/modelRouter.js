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

router.post('/upload-model', upload_model.single('data-model'), async (req, res) => {
    if (req.file) {
        const extAccept = ['.pt', '.pth']
        const extname = path.extname(req.file.originalname).toLowerCase()

        if (extAccept.includes(extname)) {
            await fs.rename(
                path.join(__dirname, '../public/model/', req.file.originalname),
                path.join(__dirname, '../public/model/', 'best.pt'),
                (err) => {
                    if (err) throw err;
                }
            );
            if (await fs.existsSync(path.join(__dirname, "../../best.pt"))) {
                await fs.unlinkSync(path.join(__dirname, "../../best.pt"));
            }

            const path_src = path.join(__dirname, "../public/model/best.pt");
            const path_dst = path.join(__dirname, "../../best.pt");
            await fs.copyFile(path_src, path_dst, (err) => {
                if (err) {
                    console.log(err);
                }
                console.log("Copy file done.");
            });
            const justAdd = true
            return res.render('upload-model', {
                justAdd
            });
        } else {
            if (await fs.existsSync(path.join(__dirname, "../../best.pt"))) {
                await fs.unlinkSync(path.join(__dirname, "../../best.pt"));
            }
            await fs.unlinkSync(path.join(__dirname, '../../', req.file.originalname));
            const notSupport = true
            return res.render('upload-model', {
                notSupport
            });
        }
    } else {
        const notFile = true
        return res.render("upload-model", {
            notFile,
        });
    }


});


module.exports = router;
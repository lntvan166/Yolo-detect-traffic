const express = require("express");
const router = express.Router();
const { upload_image } = require("../services/multer");
const fs = require("fs");
const path = require("path");

router.get("/upload-image", (req, res) => {
  const hasImage = fs.existsSync(path.join(__dirname, "../../image.png"));
  return res.render("upload-image", {
    hasImage,
  });
});

router.post("/upload-image", upload_image.single("data-image"), (req, res) => {
  const extAccept = [".png", ".jpeg", ".jpg"];
  const extname = path.extname(req.file.originalname).toLowerCase();

  if (extAccept.includes(extname)) {
		fs.unlinkSync(path.join(__dirname, "../public/model/image.png"));
    fs.rename(
      path.join(__dirname, "../public/img/", req.file.originalname),
      path.join(__dirname, "../public/img/", "image.png"),
      (err) => {
        if (err) throw err;
      }
    );
    fs.unlinkSync(path.join(__dirname, "../../image.png"));
    const path_src = path.join(__dirname, "../public/img/image.png");
    const path_dst = path.join(__dirname, "../../image.png");
    fs.copyFile(path_src, path_dst, (err) => {
      if (err) {
        console.log(err);
      }
      console.log("Copy file done.");
    });
    const hasImage = true;
    return res.render("upload-image", {
      hasImage,
    });
  } else {
    fs.unlinkSync(path.join(__dirname, "../../", req.file.originalname));
    const notSupport = true;
    return res.render("upload-image", {
      notSupport,
    });
  }
});

module.exports = router;

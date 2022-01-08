const express = require("express");
const router = express.Router();
const fs = require("fs");
const path = require("path");

/* GET home page. */
router.get("/", (req, res) => {
  const imgExist = fs.existsSync(
    path.join(__dirname, "../../image.png")
  );
  const mdlExist = fs.existsSync(path.join(__dirname, "../../best.pt"));
  const run = imgExist && mdlExist;
  return res.render("home", {
    imgExist,
    mdlExist,
    run,
  });
});

router.post("/run-model", async (req, res) => {
  const path_script = path.join(__dirname, "../../client.py");

  const child = require("child_process").exec(`python ${path_script}`);
  child.stdout.pipe(process.stdout);
  child.on("exit", function () {
    console.log("client exit");
		// const path_src = path.join(__dirname, "../../traffic-sign.png");
		// const path_dst = path.join(__dirname, "../public/result/image.png");
    // fs.copyFile(path_src, path_dst, (err) => {
    //   if (err) {
    //     console.log(err);
    //   }
		// 	console.log('Copy file done.');
    // });
    res.render("predict");
  });
});

module.exports = router;

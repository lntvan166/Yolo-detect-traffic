document.getElementById("run-model").onclick = function (event) {
    event.preventDefault();
    document.getElementById("run-model-loading").style.display = "block";
    this.form.submit();
}
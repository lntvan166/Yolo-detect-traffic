const file = document.getElementById('file-upload-btn')
const output = document.getElementById('blah')
const label = document.getElementById('image-label')

var loadFile = function(event) {
    output.src = URL.createObjectURL(event.target.files[0]);
    output.style.display = 'inline';
    label.innerHTML = event.target.files[0].name;
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
};


// document.getElementById('upload-model-btn').onclick = (ev) => {
//   ev.preventDefault()
//   document.getElementById('select-file-label').innerHTML = 'Model submitted'
//   document.getElementById('had-file').style.display = 'block'
//   document.getElementById('file-upload-form').submit()
//   this.form.submit()
// }
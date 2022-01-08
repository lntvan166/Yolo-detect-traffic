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

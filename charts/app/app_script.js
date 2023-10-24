document.addEventListener('DOMContentLoaded', function() {
    const folderInput = document.getElementById('folderInput');

    folderInput.addEventListener('change', function() {
        // Log all the file names selected
        for (let i = 0; i < this.files.length; i++) {
            console.log(this.files[i].name);
        }
    });
});
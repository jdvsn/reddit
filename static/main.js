document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.file-droppable').forEach(function(droppable) {
      var originalText = droppable.querySelector('div').innerHTML;
      var input = droppable.querySelector('input');
      var fileChanged = function() {
        var files = input.files;
        if (files.length) {
          droppable.querySelector('span').style.display = 'block';
          droppable.querySelector('#image-upload-preview').style.display = 'block';
          droppable.querySelector('div').innerHTML = '';
          droppable.classList.add('filled');
          
        } else {
          droppable.querySelector('div').innerHTML = originalText;
          droppable.classList.remove('filled');
          droppable.querySelector('span').style.display = 'none';
          droppable.querySelector('#image-upload-preview').style.display = 'none';
        }
      };
      input.addEventListener('change', fileChanged);
      fileChanged(input);
      droppable.querySelector('span').addEventListener('click', function() {
            input.value = '';
          fileChanged(input);
      });
    });
  });

function readURL(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $('#image-upload-preview').attr('src', e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
  }

function hideComment(id) {
    var id = id.slice(11);
    var comment = document.getElementById('comment' + id);
    var info = document.getElementById('infoComment' + id);
    var collapse = document.getElementById('hideComment' + id)
    comment.style.display = "none";
    info.style.display = "block";
    collapse.style.display = "none";
}

function showComment(id) {
    var id = id.slice(11);
    var comment = document.getElementById('comment' + id);
    var info = document.getElementById('infoComment' + id);
    var collapse = document.getElementById('hideComment' + id);
    comment.style.display = "block";
    info.style.display = "none";
    collapse.style.display = "block";
}
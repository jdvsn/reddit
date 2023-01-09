document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.file-droppable').forEach(function(droppable) {
      var originalText = droppable.querySelector('div').innerHTML;
      var input = droppable.querySelector('input');
      var fileChanged = function() {
        var files = input.files;
        if (files.length) {
          droppable.classList.add('filled');
          droppable.querySelector('span').style.display = 'block';
          droppable.querySelector('div').innerHTML = '';
          droppable.querySelector('#image-upload-preview').style.display = 'block';
          droppable.querySelector('#image-upload-svg-icon').style.display = 'none';
        } else {
          droppable.classList.remove('filled');
          droppable.querySelector('span').style.display = 'none';
          droppable.querySelector('div').innerHTML = originalText;
          droppable.querySelector('#image-upload-preview').style.display = 'none';
          droppable.querySelector('#image-upload-svg-icon').style.display = 'block';
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
    var collapse = document.getElementById('hideComment' + id);
    comment.classList.add('hidden');
    info.classList.remove('hidden');
    collapse.classList.add('hidden');
}

function showComment(id) {
    var id = id.slice(11);
    var comment = document.getElementById('comment' + id);
    var info = document.getElementById('infoComment' + id);
    var collapse = document.getElementById('hideComment' + id);
    comment.classList.remove('hidden');
    info.classList.add('hidden');
    collapse.classList.remove('hidden');
}
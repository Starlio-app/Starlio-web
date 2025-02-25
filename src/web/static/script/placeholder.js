const wallpaper = document.querySelector('.wallpaper-img');
const placeholder = document.querySelector('.wallpaper-placeholder');

const image = new Image();
image.src = wallpaper.src;
image.onload = function() {
  placeholder.style.display = 'none';
  wallpaper.style.display = 'block'
}
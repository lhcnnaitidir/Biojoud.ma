const droneVideo = document.querySelector('.drone-rental-media video');
const motionButton = document.querySelector('.drone-rental-motion');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

function applyMotionPreference() {
  droneVideo.autoplay = !reducedMotion.matches;
  if (reducedMotion.matches) droneVideo.pause();
}

function updateButton() {
  motionButton.setAttribute('aria-label', droneVideo.paused ? motionButton.dataset.resume : motionButton.dataset.pause);
  motionButton.querySelector('[data-icon="pause"]').toggleAttribute('hidden', droneVideo.paused);
  motionButton.querySelector('[data-icon="resume"]').toggleAttribute('hidden', !droneVideo.paused);
}

applyMotionPreference();
updateButton();
motionButton.hidden = false;
reducedMotion.addEventListener('change', applyMotionPreference);
droneVideo.addEventListener('playing', updateButton);
droneVideo.addEventListener('pause', updateButton);
motionButton.addEventListener('click', () => {
  if (droneVideo.paused) droneVideo.play().catch(updateButton);
  else droneVideo.pause();
});

export const easeInOutQuad = (t) =>
	t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

export const smoothScrollTo = (element, target, duration = 500) => {
	const start = element.scrollTop;
	const change = target - start;
	const startTime = performance.now();

	const animateScroll = (currentTime) => {
		const elapsed = currentTime - startTime;
		const progress = Math.min(elapsed / duration, 1);
		const easedProgress = easeInOutQuad(progress);
		element.scrollTop = start + change * easedProgress;
		if (progress < 1) {
			requestAnimationFrame(animateScroll);
		}
	};

	requestAnimationFrame(animateScroll);
};

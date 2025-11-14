    // JS for counting animation
  const counters = document.querySelectorAll('.stat-number');
  const speed = 60; // nižší = rychlejší

  const animateCounters = () => {
    counters.forEach(counter => {
      const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const increment = Math.ceil(target / speed);

        if (count < target) {
          counter.innerText = count + increment;
          setTimeout(updateCount, 20);
        } else {
          counter.innerText = target.toLocaleString();
        }
      };
      updateCount();
    });
  };

  const section = document.querySelector('.stats-section');
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      animateCounters();
      observer.disconnect();
    }
  });
  observer.observe(section);
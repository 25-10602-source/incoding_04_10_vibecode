document.addEventListener('DOMContentLoaded', () => {
    // 1. Header scroll effect
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Scroll Reveal Animations
    const reveals = document.querySelectorAll('.reveal');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 100;

        reveals.forEach((reveal) => {
            const elementTop = reveal.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    
    // Trigger once on load
    revealOnScroll();

    // 3. Smooth scrolling for internal links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if(targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
  
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });
    
    // 4. Hero image slow zoom effect (simulate subtle breathing)
    // We already do a simple scale in CSS, but let's augment it slightly on mouse move over hero
    const hero = document.querySelector('.hero');
    const heroBg = document.querySelector('.bg-image');
    
    if(hero && heroBg) {
        hero.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 50;
            heroBg.style.transform = `scale(1.05) translate(${xAxis}px, ${yAxis}px)`;
        });
        
        hero.addEventListener('mouseleave', () => {
            heroBg.style.transform = `scale(1.05) translate(0px, 0px)`;
            heroBg.style.transition = `transform 0.5s ease`;
        });
        
        hero.addEventListener('mouseenter', () => {
            heroBg.style.transition = `none`;
        });
    }
});

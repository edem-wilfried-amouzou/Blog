 // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
      if (navbar) {
        navbar.classList.toggle('scrolled', window.scrollY > 30);
      }
    });

    // Mobile menu toggle
    const toggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const bars = document.querySelectorAll('.menu-bar');
    if (toggle && mobileMenu) {
      const setMenuState = (open) => {
        toggle.setAttribute('aria-expanded', String(open));
        mobileMenu.classList.toggle('hidden', !open);
        if (open) {
          bars[0].style.transform = 'rotate(45deg) translate(4px, 4px)';
          bars[1].style.opacity = '0';
          bars[2].style.transform = 'rotate(-45deg) translate(4px, -4px)';
        } else {
          bars[0].style.transform = '';
          bars[1].style.opacity = '';
          bars[2].style.transform = '';
        }
      };

      toggle.addEventListener('click', () => {
        setMenuState(mobileMenu.classList.contains('hidden'));
      });

      mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
        if (!mobileMenu.classList.contains('hidden')) {
          setMenuState(false);
        }
      }));

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
          setMenuState(false);
        }
      });
    }

    // Reveal on scroll
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('reveal-visible');
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // Table of Contents Generator
    function generateTableOfContents() {
      const tocList = document.getElementById('toc-list');
      if (!tocList) return;

      // Récupère tous les h2 et h3 du contenu
      const headings = Array.from(
        document.querySelectorAll('article h2, article h3')
      );

      if (headings.length === 0) {
        tocList.innerHTML = '<li style="color: rgba(255,255,255,0.4); font-size: 0.75rem;">Aucun titre trouvé</li>';
        return;
      }

      // Crée une liste d'items pour la TOC
      tocList.innerHTML = '';
      headings.forEach((heading, idx) => {
        // Ajoute un ID au heading s'il n'en a pas
        if (!heading.id) {
          heading.id = `heading-${idx}`;
        }

        // Détermine le niveau (h2 = 0, h3 = 1)
        const level = heading.tagName === 'H2' ? 0 : 1;
        const indent = level === 0 ? '0px' : '1rem';

        // Crée l'item de la TOC
        const li = document.createElement('li');
        li.style.paddingLeft = indent;

        const a = document.createElement('a');
        a.href = `#${heading.id}`;
        a.textContent = `${level === 0 ? '▸' : '○'} ${heading.textContent}`;
        a.style.color = 'rgba(255,255,255,0.6)';
        a.style.textDecoration = 'none';
        a.style.transition = 'color 0.2s';
        a.style.display = 'block';
        a.style.paddingTop = '0.25rem';
        a.style.paddingBottom = '0.25rem';

        a.addEventListener('mouseenter', () => (a.style.color = 'var(--coral)'));
        a.addEventListener('mouseleave', () => (a.style.color = 'rgba(255,255,255,0.6)'));

        // Scroll smooth vers le heading
        a.addEventListener('click', (e) => {
          e.preventDefault();
          heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });

        li.appendChild(a);
        tocList.appendChild(li);
      });
    }

    // Génère la TOC au chargement de la page
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', generateTableOfContents);
    } else {
      generateTableOfContents();
    }
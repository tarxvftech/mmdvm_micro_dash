<header>
	<nav>

		<ul class="left">
			<li>
				<a href="/">
					Dash
				</a>
			</li>
			<li><a href="/config">Config</a></li>
			<li><a href="/services">Services</a></li>
			<li><a href="/logs">Logs</a></li>
		</ul>
		<ul class="right">
			<li><a href="/about">About</a></li>
			<li><a target="_blank" href="https://tarxvf.tech"><img title="Made with love by tarxvf" class="logo" alt="logo" src="/logo.png" /></a></li>
		</ul>
	</nav>
</header>

<slot />
<script>
    import { onMount, onDestroy } from 'svelte';

    function updateClasses() {
        const currentPath = window.location.pathname;
        const links = document.querySelectorAll('header nav ul li a');
        links.forEach(link => {
            link.parentElement.classList.toggle('thispage', link.pathname == currentPath && link.host == window.location.host);
        });
    }

    function handleNavigation() {
        // Ensure updateClasses runs after navigation
        requestAnimationFrame(updateClasses);
    }

    onMount(() => {
        updateClasses();
        window.addEventListener('popstate', handleNavigation);
        const links = document.querySelectorAll('header nav ul li a');
        links.forEach(link => {
            link.addEventListener('click', handleNavigation);
        });
    });

    onDestroy(() => {
        window.removeEventListener('popstate', handleNavigation);
        const links = document.querySelectorAll('header nav ul li a');
        links.forEach(link => {
            link.removeEventListener('click', handleNavigation);
        });
    });
</script>

import Link from 'next/link';
import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <nav className={styles.nav}>
        <Link href="/" className={styles.link}>Strona Główna</Link>
        <Link href="/people" className={styles.link}>Osoby</Link>
        <Link href="/companies" className={styles.link}>Firmy</Link>
        <Link href="/towns" className={styles.link}>Miejscowości</Link>
      </nav>
    </header>
  );
};

export default Header;
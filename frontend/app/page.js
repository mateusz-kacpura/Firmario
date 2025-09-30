import Link from 'next/link';
import styles from './Home.module.css';

export default function HomePage() {
  return (
    <div className={styles.container}>
      <h1>Witaj w aplikacji do zarządzania danymi</h1>
      <p>Wybierz jedną z sekcji, aby rozpocząć:</p>
      <div className={styles.links}>
        <Link href="/people" className={styles.card}>
          <h2>Osoby &rarr;</h2>
          <p>Zarządzaj listą osób.</p>
        </Link>
        <Link href="/companies" className={styles.card}>
          <h2>Firmy &rarr;</h2>
          <p>Przeglądaj firmy i ich oddziały.</p>
        </Link>
        <Link href="/towns" className={styles.card}>
          <h2>Miejscowości &rarr;</h2>
          <p>Zarządzaj listą dostępnych miejscowości.</p>
        </Link>
      </div>
    </div>
  );
}
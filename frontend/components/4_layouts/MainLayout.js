import Header from '../3_organisms/Header';
import styles from './MainLayout.module.css';

const MainLayout = ({ children }) => {
  return (
    <>
      <Header />
      <main className={styles.main}>{children}</main>
    </>
  );
};

export default MainLayout;
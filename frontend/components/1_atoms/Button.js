import styles from './Button.module.css';

const Button = ({ children, onClick, variant = 'primary', type = 'button' }) => {
  return (
    <button type={type} onClick={onClick} className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
};

export default Button;
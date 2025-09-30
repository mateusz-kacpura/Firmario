import styles from './Input.module.css';

const Input = ({ type = 'text', value, onChange, placeholder, name }) => {
  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      name={name}
      className={styles.input}
    />
  );
};

export default Input;
import styles from './Select.module.css';

const Select = ({ value, onChange, name, options = [], placeholder }) => {
  return (
    <select
      value={value}
      onChange={onChange}
      name={name}
      className={styles.select}
    >
      <option value="">-- {placeholder || 'Wybierz'} --</option>
      {options.map((option) => (
        <option key={option.id} value={option.id}>
          {option.name}
        </option>
      ))}
    </select>
  );
};

export default Select;
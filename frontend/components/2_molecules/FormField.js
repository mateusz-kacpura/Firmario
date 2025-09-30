import Input from '../1_atoms/Input';
import Select from '../1_atoms/Select';
import styles from './FormField.module.css';

const FormField = ({ label, type, value, onChange, name, placeholder, options }) => {
  return (
    <div className={styles.formField}>
      <label className={styles.label} htmlFor={name}>{label}</label>
      {type === 'select' ? (
        <Select
          value={value}
          onChange={onChange}
          name={name}
          options={options}
          placeholder={placeholder}
        />
      ) : (
        <Input
          type={type}
          value={value}
          onChange={onChange}
          name={name}
          placeholder={placeholder}
        />
      )}
    </div>
  );
};

export default FormField;
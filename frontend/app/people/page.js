'use client';

import { useEffect, useState } from 'react';
import { getPeople, createPerson, deletePerson, getTowns, getCompanies } from '../../lib/api';
import Button from '../../components/1_atoms/Button';
import FormField from '../../components/2_molecules/FormField';
import styles from './People.module.css';

export default function PeoplePage() {
  const [people, setPeople] = useState([]);
  const [townsOptions, setTownsOptions] = useState([]);
  const [branchesOptions, setBranchesOptions] = useState([]);
  const [error, setError] = useState(null);

  // Stan formularza
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    birth_date: '',
    town_id: '',
    company_branch_id: '',
  });

  const fetchPeople = async () => {
    try {
      const response = await getPeople();
      setPeople(response.data);
    } catch (err) {
      setError('Nie udało się pobrać listy osób.');
    }
  };

  // Pobieramy dane słownikowe (miasta i oddziały)
  const fetchFormData = async () => {
    try {
        const [townsRes, companiesRes] = await Promise.all([
            getTowns(),
            getCompanies()
        ]);
        
        setTownsOptions(townsRes.data);

        // Spłaszczamy strukturę Firmy -> Oddziały, aby stworzyć prostą listę opcji
        const allBranches = companiesRes.data.flatMap(company => 
            company.branches.map(branch => ({
                id: branch.id,
                name: `${company.name} - ${branch.name}`
            }))
        );
        setBranchesOptions(allBranches);

    } catch (err) {
        setError('Nie udało się pobrać danych formularza (miast lub firm).');
    }
  };

  useEffect(() => {
    fetchPeople();
    fetchFormData();
  }, []);

  const handleInputChange = (e) => {
      const { name, value } = e.target;
      setFormData(prev => ({
          ...prev,
          [name]: value
      }));
  };

  const handleCreatePerson = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      // Konwersja ID na liczby, backend tego oczekuje
      const payload = {
          ...formData,
          town_id: parseInt(formData.town_id),
          company_branch_id: parseInt(formData.company_branch_id),
      };
      
      await createPerson(payload);
      
      // Reset formularza
      setFormData({
        first_name: '',
        last_name: '',
        birth_date: '',
        town_id: '',
        company_branch_id: '',
      });
      fetchPeople();
    } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
             // Jeśli to błąd walidacji z backendu (np. zła data lub brakujące ID)
             const detail = err.response.data.detail;
             setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
        } else {
             setError('Nie udało się dodać osoby. Sprawdź poprawność danych.');
        }
    }
  };

  const handleDeletePerson = async (id) => {
      if (window.confirm('Czy na pewno chcesz usunąć tę osobę?')) {
        try {
            await deletePerson(id);
            fetchPeople();
        } catch (err) {
            setError('Nie udało się usunąć osoby.');
        }
      }
  };

  return (
    <div>
      <h1>Osoby</h1>
      {error && <p className={styles.error}>{error}</p>}
      
      <form onSubmit={handleCreatePerson} className={styles.form}>
        <h2>Dodaj nową osobę</h2>
        <FormField
          label="Imię"
          name="first_name"
          value={formData.first_name}
          onChange={handleInputChange}
        />
        <FormField
          label="Nazwisko"
          name="last_name"
          value={formData.last_name}
          onChange={handleInputChange}
        />
        <FormField
          label="Data urodzenia"
          type="date"
          name="birth_date"
          value={formData.birth_date}
          onChange={handleInputChange}
        />
        <FormField
            label="Miejscowość"
            type="select"
            name="town_id"
            value={formData.town_id}
            onChange={handleInputChange}
            options={townsOptions}
            placeholder="Wybierz miejscowość"
        />
         <FormField
            label="Oddział Firmy"
            type="select"
            name="company_branch_id"
            value={formData.company_branch_id}
            onChange={handleInputChange}
            options={branchesOptions}
            placeholder="Wybierz oddział"
        />
        <Button type="submit">Dodaj osobę</Button>
      </form>

      <div className={styles.list}>
        {people.map((person) => (
          <div key={person.id} className={styles.personCard}>
            <div className={styles.personHeader}>
                <h3>{person.first_name} {person.last_name}</h3>
                <Button onClick={() => handleDeletePerson(person.id)} variant="danger">
                Usuń
                </Button>
            </div>
            <div className={styles.personDetails}>
                <p><strong>Wiek:</strong> {person.age} lat</p>
                <p><strong>Płeć:</strong> {person.gender}</p>
                <p><strong>Miejscowość:</strong> {person.miejscowosc}</p>
                <p><strong>Firma:</strong> {person.firma} ({person.oddzial_firmy})</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
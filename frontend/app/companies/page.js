'use client';

import { useEffect, useState } from 'react';
import { getCompanies, createCompany, deleteCompany } from '../../lib/api';
import Button from '../../components/1_atoms/Button';
import FormField from '../../components/2_molecules/FormField';
import styles from './Companies.module.css';
import Link from 'next/link';

export default function CompaniesPage() {
  const [companies, setCompanies] = useState([]);
  const [newCompanyName, setNewCompanyName] = useState('');
  const [error, setError] = useState(null);

  const fetchCompanies = async () => {
    try {
      const response = await getCompanies();
      setCompanies(response.data);
    } catch (err) {
      setError('Nie udało się pobrać firm.');
    }
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const handleCreateCompany = async (e) => {
    e.preventDefault();
    if (!newCompanyName) return;
    try {
      await createCompany({ name: newCompanyName });
      setNewCompanyName('');
      fetchCompanies(); // Odśwież listę
    } catch (err) {
      setError('Nie udało się dodać firmy.');
    }
  };

  const handleDeleteCompany = async (id) => {
    if (window.confirm('Czy na pewno chcesz usunąć tę firmę i wszystkie jej oddziały?')) {
        try {
            await deleteCompany(id);
            fetchCompanies(); // Odśwież listę
        } catch (err) {
            setError('Nie udało się usunąć firmy.');
        }
    }
  };

  return (
    <div>
      <h1>Firmy</h1>
      {error && <p className={styles.error}>{error}</p>}
      
      <form onSubmit={handleCreateCompany} className={styles.form}>
        <FormField
          label="Nazwa nowej firmy"
          type="text"
          value={newCompanyName}
          onChange={(e) => setNewCompanyName(e.target.value)}
          placeholder="Wprowadź nazwę firmy"
        />
        <Button type="submit">Dodaj firmę</Button>
      </form>

      <ul className={styles.list}>
        {companies.map((company) => (
          <li key={company.id} className={styles.listItem}>
            <div>
              <Link href={`/companies/${company.id}`} className={styles.link}>
                <strong>{company.name}</strong>
              </Link>
              <span>(Oddziały: {company.branches.length})</span>
            </div>
            <Button onClick={() => handleDeleteCompany(company.id)} variant="danger">
              Usuń
            </Button>
          </li>
        ))}
      </ul>
    </div>
  );
}
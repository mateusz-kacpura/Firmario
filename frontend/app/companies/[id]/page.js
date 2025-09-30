'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getCompany, getCompanyBranches, createCompanyBranch, deleteBranch } from '../../../lib/api';
import Button from '../../../components/1_atoms/Button';
import FormField from '../../../components/2_molecules/FormField';
import styles from './CompanyDetails.module.css';

export default function CompanyDetailsPage({ params }) {
  const companyId = params.id;
  const [company, setCompany] = useState(null);
  const [branches, setBranches] = useState([]);
  const [newBranchName, setNewBranchName] = useState('');
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const [companyRes, branchesRes] = await Promise.all([
        getCompany(companyId),
        getCompanyBranches(companyId)
      ]);
      setCompany(companyRes.data);
      setBranches(branchesRes.data);
    } catch (err) {
      setError('Nie udało się pobrać danych firmy.');
    }
  };

  useEffect(() => {
    if (companyId) {
        fetchData();
    }
  }, [companyId]);

  const handleCreateBranch = async (e) => {
    e.preventDefault();
    if (!newBranchName) return;
    try {
      await createCompanyBranch(companyId, { name: newBranchName });
      setNewBranchName('');
      fetchData(); 
    } catch (err) {
      setError('Nie udało się dodać oddziału.');
    }
  };

  const handleDeleteBranch = async (branchId) => {
      if (window.confirm('Czy na pewno chcesz usunąć ten oddział?')) {
        try {
            await deleteBranch(branchId);
            fetchData();
        } catch (err) {
            setError('Nie udało się usunąć oddziału.');
        }
      }
  };

  if (!company) return <div>Ładowanie...</div>;

  return (
    <div>
        <Link href="/companies" className={styles.backLink}>&larr; Wróć do listy firm</Link>
        <h1>Firma: {company.name}</h1>
        <h2>Oddziały</h2>
        {error && <p className={styles.error}>{error}</p>}
      
        <form onSubmit={handleCreateBranch} className={styles.form}>
            <FormField
            label="Nazwa nowego oddziału"
            type="text"
            value={newBranchName}
            onChange={(e) => setNewBranchName(e.target.value)}
            placeholder="Np. Centrala"
            />
            <Button type="submit">Dodaj oddział</Button>
        </form>

        <ul className={styles.list}>
            {branches.map((branch) => (
            <li key={branch.id} className={styles.listItem}>
                <span>{branch.name}</span>
                <Button onClick={() => handleDeleteBranch(branch.id)} variant="danger">
                Usuń
                </Button>
            </li>
            ))}
        </ul>
    </div>
  );
}
'use client';

import { useEffect, useState } from 'react';
import { getTowns, createTown, deleteTown } from '../../lib/api';
import Button from '../../components/1_atoms/Button';
import FormField from '../../components/2_molecules/FormField';
import styles from './Towns.module.css';

export default function TownsPage() {
  const [towns, setTowns] = useState([]);
  const [newTownName, setNewTownName] = useState('');
  const [error, setError] = useState(null);

  const fetchTowns = async () => {
    try {
      const response = await getTowns();
      setTowns(response.data);
      setError(null);
    } catch (err) {
      setError('Nie udało się pobrać miejscowości.');
    }
  };

  useEffect(() => {
    fetchTowns();
  }, []);

  const handleCreateTown = async (e) => {
    e.preventDefault();
    if (!newTownName) return;
    try {
      await createTown({ name: newTownName });
      setNewTownName('');
      fetchTowns();
    } catch (err) {
        // Backend zwraca 409 jeśli nazwa już istnieje
        if (err.response && err.response.status === 409) {
             setError(err.response.data.detail);
        } else {
             setError('Nie udało się dodać miejscowości.');
        }
    }
  };

  const handleDeleteTown = async (id) => {
      if (window.confirm('Czy na pewno chcesz usunąć tę miejscowość?')) {
        try {
            await deleteTown(id);
            fetchTowns();
        } catch (err) {
            setError('Nie udało się usunąć miejscowości. Upewnij się, że nie są do niej przypisane żadne osoby.');
        }
      }
  };

  return (
    <div>
      <h1>Miejscowości</h1>
      {error && <p className={styles.error}>{error}</p>}
      
      <form onSubmit={handleCreateTown} className={styles.form}>
        <FormField
          label="Nazwa nowej miejscowości"
          type="text"
          value={newTownName}
          onChange={(e) => setNewTownName(e.target.value)}
          placeholder="Np. Warszawa"
        />
        <Button type="submit">Dodaj miejscowość</Button>
      </form>

      <ul className={styles.list}>
        {towns.map((town) => (
          <li key={town.id} className={styles.listItem}>
            <span>{town.name}</span>
            <Button onClick={() => handleDeleteTown(town.id)} variant="danger">
              Usuń
            </Button>
          </li>
        ))}
      </ul>
    </div>
  );
}
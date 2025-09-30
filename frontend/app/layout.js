import MainLayout from '../components/4_layouts/MainLayout';
import './globals.css';

export const metadata = {
  title: 'Zarządzanie Danymi',
  description: 'Frontend dla aplikacji rekrutacyjnej',
};

export default function RootLayout({ children }) {
  return (
    <html lang="pl">
      <body>
        <MainLayout>{children}</MainLayout>
      </body>
    </html>
  );
}
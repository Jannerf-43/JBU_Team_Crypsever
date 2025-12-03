import './globals.css'
import { ClerkProvider } from '@clerk/nextjs'

export const metadata = {
  title: 'CrypServer',
  description: 'AES+RSA 암호화 파일 서버',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="ko">
        <body className="min-h-screen">{children}</body>
      </html>
    </ClerkProvider>
  )
}

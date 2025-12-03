import './globals.css'
import { ClerkProvider } from '@clerk/nextjs'

export const metadata = {
  title: 'CrypServer',
  description: 'AES+RSA Hybrid Encryption Storage',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="ko">
        <body
          className="min-h-screen bg-fixed bg-center bg-cover"
          style={{
            backgroundImage: 'url("/bg.jpg")', // public/bg.jpg
          }}
        >
          {/* 어두운 필터(가독성 향상용) */}
          <div className="min-h-screen bg-black/50">{children}</div>
        </body>
      </html>
    </ClerkProvider>
  )
}

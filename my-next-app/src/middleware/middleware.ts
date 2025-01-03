import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const isAuthPath = request.nextUrl.pathname.startsWith('/studio');
  const isLoginPath = request.nextUrl.pathname === '/login';

  // If no token and trying to access protected route
  if (isAuthPath && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // If has token and trying to access login
  if (isLoginPath && token) {
    return NextResponse.redirect(new URL('/studio', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/studio/:path*', '/login']
};
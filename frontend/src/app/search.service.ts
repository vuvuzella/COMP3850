import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Location} from './location';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class SearchService {

  private locationsUrl = 'api/locations';

  constructor( private http: HttpClient ) { }

  getLocations(): Observable<Location[]> {
    return this.http.get<Location[]>(this.locationsUrl);
  }

  /* GET heroes whose name contains search term */
  searchLocations(term: string): Observable<Location[]> {
    if (!term.trim()) {
      // if not search term, return empty hero array.
      return of([]);
    }
    return this.http.get<Location[]>(`${this.locationsUrl}/?name=${term}`).pipe();
  }
}
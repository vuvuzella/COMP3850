import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { Location} from './location';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class SearchService {

  private locationsUrl = 'api/locations';  // URL to web api

  constructor(
    private http: HttpClient ) { }

  /** GET heroes from the server */
  getLocations(): Observable<Location[]> {
    return this.http.get<Location[]>(this.locationsUrl);
  }

  /** GET Location by id. Will 404 if id not found */
  getLocation(id: number): Observable<Location> {
    const url = `${this.locationsUrl}/${id}`;
    return this.http.get<Location>(url);
  }

  /* GET heroes whose name contains search term */
  searchLocations(term: string): Observable<Location[]> {
    if (!term.trim()) {
      // if not search term, return empty Location array.
      return of([]);
    }
    return this.http.get<Location[]>(`${this.locationsUrl}/?area_name=${term}`)
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

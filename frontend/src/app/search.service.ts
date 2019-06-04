import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Area } from './models/area';
import { environment } from 'src/environments/environment';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class SearchService {

  apiUrl: string = environment.areas;
  constructor(
    private http: HttpClient ) { }

  getAllAreas(){
    return this.http.get<Area[]>(`${this.apiUrl}/areas`)
  }
}

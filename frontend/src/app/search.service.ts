import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

import { Area } from './models/area';
import { Cluster } from './models/cluster'
import { Path } from './models/path'
import { Points } from './models/points'
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
    return this.http.get<Area[]>(`${this.apiUrl}/runareas`)
  }

  getAreaClusters(areaName: string){
    return this.http.get<Cluster[]>(`${this.apiUrl}/clusters`, {
      params: { area: areaName }
    })
  }

  getClusterPaths(clusterID){
    return this.http.get<Path[]>(`${this.apiUrl}/runpaths`, {
      params: { cluster: clusterID }
    })
  }

  getPathPoints(pathID) {
    return this.http.get<Points[]>(`${this.apiUrl}/points`, {
      params: { path: pathID }
    })
  }
}

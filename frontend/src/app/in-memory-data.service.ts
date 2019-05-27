import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Location } from './location';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const locations = [
      { id: 1, city: "Newcastle", area_name: "Birmingham Gardens", longitude: 151.6919, latitude: 20.1234 },
      { id: 2, city: "Newcastle", area_name: "Wallsend", longitude: 151.1234, latitude: 12.1342 }
    ];
    return {locations};
  }
}

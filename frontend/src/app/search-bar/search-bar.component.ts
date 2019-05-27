import { Component, OnInit } from '@angular/core';

import { Observable, Subject } from 'rxjs';

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';

import { Location } from '../location';
//import { SearchService } from '../search.service';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.css']
})
export class SearchBarComponent implements OnInit {

  location$: Observable<Location[]>;
  private searchTerms = new Subject<string>();

  constructor(/*private searchService: SearchService*/) {}

  // Push a search term into the observable stream.
  search(term: string): void {
    this.searchTerms.next(term);
  }

  ngOnInit(): void {
   //this.location$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
    // debounceTime(300),

      // ignore new term if same as previous term
     // distinctUntilChanged(),

      // switch to new search observable each time the term changes
      //switchMap((term: string) => this.searchService.searchLocations(term)),
   // );
  }
}
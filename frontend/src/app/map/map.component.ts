import { Component, OnInit } from '@angular/core';
import { } from 'googlemaps';
import { ViewChild } from '@angular/core';
import { initDomAdapter } from '@angular/platform-browser/src/browser';

declare function initMap(): any;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {

    initMap();

 }
}

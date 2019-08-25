import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeTopBarComponent } from './home-top-bar.component';

describe('HomeTopBarComponent', () => {
  let component: HomeTopBarComponent;
  let fixture: ComponentFixture<HomeTopBarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HomeTopBarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeTopBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

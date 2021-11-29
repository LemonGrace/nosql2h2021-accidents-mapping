import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {IItemsModelsResponse, IItemsResponse, ProductService} from "../product.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-brand',
  templateUrl: './brand.component.html',
  styleUrls: ['./brand.component.css']
})
export class BrandComponent implements OnInit {
  @ViewChild('input') public $InputElement: ElementRef | undefined;
  public Models: IItemsModelsResponse[] | undefined;
  public Init: boolean = false;
  public Brand: string;
  public Result: IItemsModelsResponse[] | undefined;
  private readonly _brandName: string | undefined;

  constructor(
    protected productService: ProductService,
    protected router: Router,
    protected nav: Router
  ) {
    this._brandName = this.router.url
    this.Brand = this.router.url.split("/")[1]
  }

  public async ngOnInit(): Promise<void> {
    console.log(this._brandName)
    console.log(this.Brand)
    if (!this._brandName) {
      return;
    }
    this.Models = await this.productService.GetModels(this._brandName);
    this.Init = true;
  }

  public async GoToGenerations(modelName: string): Promise<void> {
    await this.nav.navigate([this._brandName, modelName])
  }

  public FindModel(e: Event): void {
    const value = this.$InputElement?.nativeElement.value;
    console.log(value)
    if (!value){
      this.Result = [];
      return;
    }
    if (!this.Models)
      return;
    this.Result = this.Models.filter(_model => _model.modelName.includes(value));
  }

}

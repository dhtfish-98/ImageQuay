// Owned static ObjC oracle; compiled to a dylib, never loaded or run.
#import <Foundation/Foundation.h>
@protocol QuayBase
@property(nonatomic, readonly) NSInteger tag;
- (void)updateValue:(NSInteger)value;
@optional
+ (id)make;
@end
@protocol QuayChild <QuayBase>
@property(class, readonly) id shared;
@end
@interface QuayRoot : NSObject <QuayChild>
@property(nonatomic) int counter;
@property(nonatomic, copy) NSString *title;
@property(nonatomic, readonly) NSInteger tag;
- (void)updateValue:(NSInteger)value;
+ (id)shared;
@end
@implementation QuayRoot
- (NSInteger)tag { return self.counter; }
- (void)updateValue:(NSInteger)value { self.counter = (int)value; }
+ (id)shared { return nil; }
@end
@interface QuayRoot (Extra)
@property(nonatomic, readonly) int doubled;
- (int)add:(int)value;
@end
@implementation QuayRoot (Extra)
- (int)doubled { return self.counter * 2; }
- (int)add:(int)value { return self.counter + value; }
@end
@interface NSObject (QuayExternal)
@property(nonatomic, readonly) int quayMarker;
- (int)quayAdd:(int)value;
@end
@implementation NSObject (QuayExternal)
- (int)quayMarker { return 1; }
- (int)quayAdd:(int)value { return value + 1; }
@end
